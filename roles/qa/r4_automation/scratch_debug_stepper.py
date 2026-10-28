from playwright.sync_api import sync_playwright
from pages.real_login import goto_signed_in
from pages.real_schemes import Wizard

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome")
    page = browser.new_page()
    wiz = Wizard(page, "http://localhost:5173").open()
    wiz.name.fill("")
    wiz.go_next()
    page.wait_for_timeout(1000)

    stepper = wiz.stepper
    print("stepper count:", stepper.count())
    lis = stepper.locator("li").all()
    print("lis count:", len(lis))
    for li in lis:
        print("li text:", repr(li.text_content()))
        print("li has 'General':", "General" in li.text_content())
        err = li.get_by_text("This step has errors")
        print("err count:", err.count())

    flt = stepper.locator("li").filter(has_text="General")
    print("flt count:", flt.count())
    print("flt err count:", flt.get_by_text("This step has errors").count())

    browser.close()
