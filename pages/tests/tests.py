import re

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def home_page(page: Page):
    page.goto("https://playwright.dev/")
    return page


class TestPlaywrightSiteHomePage:
    def test_has_title(self, home_page: Page):
        expect(home_page).to_have_title(re.compile("Playwright"))

    def test_get_started_link(self, home_page: Page):
        home_page.get_by_role("link", name="Get started").click()
        expect(home_page.get_by_role("heading", name="Installation")).to_be_visible()

    def test_git_hub_link(self, home_page: Page):
        with home_page.expect_popup() as page1_info:
            home_page.get_by_role("link", name="GitHub repository").click()
        git_page = page1_info.value
        expect(git_page.locator("#repository-container-header")).to_contain_text(
            "microsoft / playwright Public"
        )
        expect(
            git_page.get_by_role("link", name=".github, (Directory)")
        ).to_be_visible()

    def test_node_js_dropdown(self, home_page: Page):
        assert not home_page.get_by_role("link", name="Node.js").is_visible()
        home_page.locator("button").hover()
        expect(home_page.get_by_role("link", name="Node.js")).to_be_visible()

    def test_type_script_link(self, home_page: Page):
        home_page.get_by_role("link", name="TypeScript").click()
        with home_page.expect_popup() as page1_info:
            home_page.get_by_role("link", name="Playwright Training").click()
        page1 = page1_info.value
        expect(page1.locator("h1")).to_contain_text(
            "Build Your first end-to-end test with Playwright"
        )
        page1.locator('[data-test-id="header-link-browse-all-training"]').click()
        expect(page1.locator("h1")).to_contain_text("Browse all training")
