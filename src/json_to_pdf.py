import json
import atexit
from typing import Optional

import chevron
from playwright.sync_api import sync_playwright, Browser, Playwright

browser: Optional[Browser] = None
playwright: Optional[Playwright] = None


def release_chromium():
    global browser, playwright
    try:
        if browser is not None:
            browser.close()
            browser = None
            print('Browser stopped')
        if playwright is not None:
            playwright.stop()
            playwright = None
    except Exception as e:
        print(f'Cannot close browser: {e}')


def init_chromium():
    release_chromium()
    global browser, playwright
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch()
        atexit.register(release_chromium)
        print('Browser launched')
    except Exception as e:
        print(f'Cannot start browser: {e}')


def html_to_pdf(html: str, output_path: str) -> str | None:
    global browser
    if browser is None:
        init_chromium()
    try:
        page = browser.new_page()
        page.set_content(html)
        header = '''
                 <div style="
                     text-align: right;
                     width: 30cm;
                     font-size: 14px;">
                     <span style="margin-right: 2cm">
                         Page <b><span class="pageNumber"></span></b>
                     </span>
                 </div>
             '''
        page.pdf(path=output_path, display_header_footer=True, header_template=header, footer_template=' ')
        page.close()
    except Exception as e:
        print(f'Cannot create pdf from html: {e}')
        return None
    return output_path


def json_to_html(jsond: str, template: str) -> str | None:
    try:
        with open(jsond, 'r') as f:
            jsond = json.loads(f.read())
        with open(template, 'r') as f:
            template = f.read()
        return chevron.render(template, jsond)
    except Exception as e:
        print(f'Cannot create html from json: {e}')
    return None


def json_to_pdf(jsond_path: str, template_path: str, output_path: str) -> str | None:
    html = json_to_html(jsond_path, template_path)
    return html_to_pdf(html, output_path)
