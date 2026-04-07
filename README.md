# rss-json-generator

一个通过定时将 RSS 订阅源转换为 JSON 数据的工具，解决了 RSS 数据缓存和格式转换的问题。

## 使用方法

1. 把本仓库 fork 到您的 GitHub 中。
2. 修改 `config.yml` 中的配置信息，添加需要转换的 RSS 订阅源链接。
3. 前往 Actions 页面，点击绿色的「enable workflows」按钮。
4. 刷新 Actions 页面，点击左侧「Generator」选项卡，再点击右侧的「enable workflow」按钮。
5. 点击 Star 以主动触发 Action 进行测试。

等待 Action 运行完毕，生成 output 路径以及文件就说明配置成功了。

## 支持的 RSS 格式

- RSS 2.0
- Atom 1.0

## 示例 RSS 源

```yaml
links:
  # 即刻用户动态
  - https://rsshub.261770.xyz/jike/user/07152f0c-0f65-4501-855b-031f3e20e4a5
  # 其他 RSS 源
  - https://example.com/feed.xml
```

## JSON 输出格式

```json
{
  "title": "RSS 标题",
  "link": "源链接",
  "description": "描述",
  "lastBuildDate": "最后更新时间",
  "feed_url": "RSS 源地址",
  "fetch_time": "获取时间",
  "items": [
    {
      "title": "文章标题",
      "link": "文章链接",
      "description": "文章内容",
      "pubDate": "发布时间",
      "guid": "唯一标识"
    }
  ]
}
```
