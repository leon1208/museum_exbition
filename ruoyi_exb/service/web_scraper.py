"""
网页抓取和转换模块
使用Playwright访问网页并将HTML转换为Markdown格式
"""
import asyncio
import logging
from playwright.async_api import async_playwright
from markdownify import markdownify as md

from ruoyi_common.ruoyi.config import CONFIG_CACHE

# 配置日志
logger = logging.getLogger(__name__)

# 更“完整”的浏览器头（可根据需要调整）
COMMON_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/121.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Referer": "https://www.nmpa.gov.cn/",
    # 常见客户端提示头（可选）
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    # Add Sec-CH-UA headers which some servers check
    "Sec-CH-UA": '"Chromium";v="121", "Google Chrome";v="121", "Not;A Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"'
}

class WebScraper:
    def __init__(self):
        """初始化网页抓取器"""
        pass
    
    async def _create_browser_and_page(self, playwright, timeout: int = 120000, headless: bool = True):
        """
        创建浏览器和页面对象的公共方法
        
        Args:
            playwright: Playwright实例
            timeout: 超时时间（毫秒）
            
        Returns:
            tuple: (browser, context, page) 元组
        """
        browser_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
        ]
        launch_kwargs = {"headless": headless, "args": browser_args}

        # 启动浏览器
        remote_playwright = CONFIG_CACHE.get('aicrawl.chromium.ws_endpoint', None)
        if remote_playwright:
            browser = await playwright.chromium.connect(remote_playwright)
        else:
            browser = await playwright.chromium.launch(**launch_kwargs)

        context = await browser.new_context(
            user_agent=COMMON_HEADERS["User-Agent"],
            viewport={"width": 1366, "height": 768},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            java_script_enabled=True,
            accept_downloads=True,
            bypass_csp=False,
            extra_http_headers={
                "accept-language": COMMON_HEADERS["Accept-Language"],
                # "referer": COMMON_HEADERS["Referer"],
                "sec-ch-ua": COMMON_HEADERS["Sec-CH-UA"],
                "sec-ch-ua-mobile": COMMON_HEADERS["Sec-CH-UA-Mobile"],
                "sec-ch-ua-platform": COMMON_HEADERS["Sec-CH-UA-Platform"],
            }
        )

        page = await context.new_page()
        page.set_default_timeout(timeout)
        
        return browser, context, page

    async def scrape_and_convert(self, url: str, timeout: int = 120000) -> dict:
        """
        抓取网页并将其转换为Markdown格式
        
        Args:
            url (str): 要抓取的网页URL
            timeout (int): 超时时间（毫秒）
            
        Returns:
            dict: 包含状态和结果的字典
        """
        try:
            # 验证URL格式
            if not url.startswith(('http://', 'https://')):
                return {
                    'status': 'error',
                    'message': '无效的URL格式，请确保以http://或https://开头'
                }
            
            async with async_playwright() as p:
                # 创建浏览器和页面对象
                browser, context, page = await self._create_browser_and_page(p, timeout, headless=True)

                # 记录请求/响应（更详细）
                # def on_request(request):
                #     print("[REQ] ->", request.method, request.url)
                # def on_response(response):
                #     status = response.status
                #     if status >= 400:
                #         try:
                #             body_snippet = response.text()[:1000]
                #         except Exception:
                #             body_snippet = "<no-body-or-binary>"
                #         print(f"[RESP ERROR] {status} {response.url}\n--- body snippet ---\n{body_snippet}\n--- end snippet ---")
                #     else:
                #         print(f"[RESP] {status} {response.url}")
                # page.on("request", on_request)
                # page.on("response", on_response)
                # page.on("console", lambda msg: print(f"[PAGE console] {msg.type}: {msg.text}"))
                # page.on("pageerror", lambda err: print(f"[PAGE error] {err}"))
                # page.on("requestfailed", lambda req: print(f"[REQ failed] {req.url} -> {req.failure}"))

                # 设置超时
                page.set_default_timeout(timeout)
                
                # 访问网页
                logger.info(f"正在访问网页: {url}")
                await page.goto(url, wait_until="networkidle", timeout=timeout)
                
                # 获取页面标题
                title = await page.title()
                print(f"页面标题: {title}")
                
                # 获取页面内容
                html_content = await page.content()
                
                # 关闭浏览器
                await browser.close()
                
                # 将HTML转换为Markdown
                logger.info("正在将HTML转换为Markdown...")
                markdown_content = md(html_content)
                
                return {
                    'status': 'success',
                    'title': title,
                    'markdown': markdown_content,
                    'url': url
                }
                
        except asyncio.TimeoutError:
            return {
                'status': 'error',
                'message': '页面加载超时，请检查网络连接或稍后重试'
            }
        except Exception as e:
            logger.error(f"抓取网页时发生错误: {str(e)}")
            import traceback
            logger.error(f"异常堆栈信息:\n{traceback.format_exc()}")
            return {
                'status': 'error',
                'message': f'抓取网页时发生错误: {str(e)}'
            }
    
    async def scrape_and_extract_section(self, url: str, section_title: str, keywords: list[str] = None, timeout: int = 30000) -> dict:
        """
        抓取网页，转换为Markdown，并提取指定栏目下的内容
        
        Args:
            url (str): 要抓取的网页URL
            section_title (str): 要提取的栏目标题
            keywords (List[str]): 用户关注的关键词列表
            timeout (int): 超时时间（毫秒）
            
        Returns:
            dict: 包含状态和提取结果的字典
        """

        # 首先抓取并转换网页
        scrape_result = await self.scrape_and_convert(url, timeout, headless=True)
        
        if scrape_result['status'] != 'success':
            return scrape_result
        
        # 将导入移到函数内部以避免循环导入
        from ai_processor import get_ai_processor
        
        # 获取AI处理器
        ai_processor = get_ai_processor()
        
        # 使用AI提取指定栏目下的内容
        extract_result = ai_processor.extract_markdown_section(
            scrape_result['markdown'], 
            section_title,
            keywords  # 传递关键词参数
        )
        
        if extract_result['status'] == 'success':
            return {
                'status': 'success',
                'title': scrape_result['title'],
                'url': scrape_result['url'],
                'section_data': extract_result['data']
            }
        else:
            return {
                'status': 'error',
                'message': f'提取栏目内容失败: {extract_result["message"]}'
            }
    
    async def auto_scroll(self, page, step=1000, delay=1.5):
        """自动往下滚动，并等待加载"""
        previous_height = await page.evaluate("() => document.body.scrollHeight")
        i=10
        while i>0:
            # 滚动到底部
            await page.evaluate(f"window.scrollBy(0, {step});")
            await asyncio.sleep(delay)
            await page.wait_for_load_state('networkidle')

            # 等待新内容加载
            new_height = await page.evaluate("() => document.body.scrollHeight")

            # 如果高度不再变化 → 已到底部
            if new_height == previous_height:
                break

            previous_height = new_height
            i-=1
            print(f"已滚动 {step} 像素，当前高度: {new_height}")

            # 模拟人类滚动        
    
    async def take_screenshot(self, url: str, full_page: bool = False, timeout: int = 120000) -> dict:
        """
        对指定URL的网页进行截图
        
        Args:
            url (str): 要截图的网页URL
            full_page (bool): 是否截取完整页面，默认为False
            timeout (int): 超时时间（毫秒）
            
        Returns:
            dict: 包含状态和Base64编码的截图数据
        """
        try:
            # 验证URL格式
            if not url.startswith(('http://', 'https://')):
                return {
                    'status': 'error',
                    'message': '无效的URL格式，请确保以http://或https://开头'
                }
            
            async with async_playwright() as p:
                # 创建浏览器和页面对象
                browser, context, page = await self._create_browser_and_page(p, timeout, headless=True)
                
                # 设置超时
                await page.goto(url, timeout=timeout, wait_until="networkidle")
                
                # 等待页面加载完成
                await page.wait_for_load_state("networkidle")
                
                # 获取页面标题
                title = await page.title()

                # 自动滚动加载所有内容
                if full_page:
                    await self.auto_scroll(page)                
                    height = await page.evaluate("document.body.scrollHeight")
                    print(f"页面高度: {height}")

                # 截取页面，返回Base64编码的数据
                screenshot_data = await page.screenshot(
                    full_page=full_page,
                    type="png",
                )
                
                # 将二进制数据转换为Base64编码
                import base64
                screenshot_base64 = base64.b64encode(screenshot_data).decode('utf-8')

                # 关闭浏览器
                await browser.close()
                
                return {
                    'title': title,
                    'url': url,
                    'screenshot': screenshot_base64
                }
                
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            # import traceback
            # logger.error(f"异常堆栈信息:\n{traceback.format_exc()}")
            raise e

# 全局网页抓取器实例
_web_scraper = None

def get_web_scraper() -> WebScraper:
    """
    获取全局网页抓取器实例
    
    Returns:
        WebScraper: 网页抓取器实例
    """
    global _web_scraper
    if _web_scraper is None:
        _web_scraper = WebScraper()
    return _web_scraper

async def scrape_url_to_markdown(url: str) -> dict:
    """
    异步抓取URL并转换为Markdown
    
    Args:
        url (str): 要抓取的网页URL
        
    Returns:
        dict: 包含状态和结果的字典
    """
    scraper = get_web_scraper()
    return await scraper.scrape_and_convert(url)

async def scrape_and_extract_section(url: str, section_title: str, keywords: list[str] = None) -> dict:
    """
    异步抓取URL，转换为Markdown并提取指定栏目
    
    Args:
        url (str): 要抓取的网页URL
        section_title (str): 要提取的栏目标题
        keywords (List[str]): 用户关注的关键词列表
        
    Returns:
        dict: 包含状态和提取结果的字典
    """
    scraper = get_web_scraper()
    return await scraper.scrape_and_extract_section(url, section_title, keywords)

async def take_website_screenshot(url: str, full_page: bool = False) -> dict:
    """
    异步对指定URL的网页进行截图
    
    Args:
        url (str): 要截图的网页URL
        full_page (bool): 是否截取完整页面，默认为False
        
    Returns:
        dict: 包含状态和Base64编码的截图数据
    """
    scraper = get_web_scraper()
    return await scraper.take_screenshot(url, full_page)