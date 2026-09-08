"""Run manually with .venv/Scripts/python tests/check_workshop.py.

Requires Playwright and an installed Microsoft Edge browser.
"""
import sys
from pathlib import Path
from threading import Thread

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, LESSONS
from werkzeug.serving import make_server
from playwright.sync_api import sync_playwright


def main():
    client = app.test_client()
    assert client.get('/').status_code == 200
    assert len(client.get('/api/users').json) == 3
    assert client.get('/api/users?fail=1').status_code == 503
    assert client.get('/api/users').headers['Access-Control-Allow-Origin'] == '*'
    assert len({lesson['id'] for lesson in LESSONS}) == len(LESSONS)
    assert all(len(lesson['hints']) == 3 for lesson in LESSONS)
    server = make_server('127.0.0.1', 0, app)
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel='msedge', headless=True)
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}')
            for index, lesson in enumerate(LESSONS):
                page.locator('.lesson-link').nth(index).click()
                buttons = page.locator('#hint-buttons button')
                assert buttons.nth(1).is_enabled()
                assert buttons.nth(2).is_enabled()
                buttons.nth(2).click()
                assert page.locator('#hint-2').is_visible()
                buttons.nth(2).click()
                assert page.locator('#hint-2').is_hidden()
                for hint in range(3):
                    buttons.nth(hint).click()
                    assert page.locator(f'#hint-{hint}').is_visible()
                page.locator('#code').fill(lesson['starter'])
                page.locator('#run').click()
                page.wait_for_function("!document.getElementById('run').disabled")
                page.locator('#code').fill(lesson['hints'][2])
                page.locator('#run').click()
                page.wait_for_function("!document.getElementById('run').disabled")
                assert page.locator('#feedback').get_attribute('class') == 'success', (lesson['id'], page.locator('#output').inner_text())
                print(f"PASS {lesson['id']}")
            assert page.locator('#progress-count').inner_text() == f'{len(LESSONS)} / {len(LESSONS)}'
            page.reload()
            assert page.locator('#progress-count').inner_text() == f'{len(LESSONS)} / {len(LESSONS)}'
            page.locator('.lesson-link').last.click()
            assert page.locator('#code').input_value() == LESSONS[-1]['hints'][2]
            for index in [6, 10]:
                page.locator('.lesson-link').nth(index).click()
                page.locator('#code').fill('console.log("Mitt svar");')
                page.locator('#run').click()
                page.wait_for_function("!document.getElementById('run').disabled")
                assert page.locator('#output').inner_text() == 'Mitt svar'
                assert page.locator('#feedback').get_attribute('class') == 'success'
            page.locator('.lesson-link').first.click()
            page.locator('#code').fill('console.log(42); throw new Error("testfeil");')
            page.locator('#run').click()
            page.wait_for_function("!document.getElementById('run').disabled")
            assert '42' in page.locator('#output').inner_text()
            assert 'testfeil' in page.locator('#output').inner_text()
            for index in [0, 10]:
                page.locator('.lesson-link').nth(index).click()
                for code, output, status in [
                    ('console.log("Anna svar");', 'Anna svar', 'success'),
                    ('return 123;', '123', 'success'),
                    ('console.error("Feilmelding");', 'Feilmelding', 'error'),
                    ('await Promise.resolve(); console.log("Asynkront");', 'Asynkront', 'success'),
                ]:
                    page.locator('#code').fill(code)
                    page.locator('#run').click()
                    page.wait_for_function("!document.getElementById('run').disabled")
                    assert page.locator('#output').inner_text() == output
                    assert page.locator('#feedback').get_attribute('class') == status
            page.set_viewport_size({'width': 390, 'height': 844})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
