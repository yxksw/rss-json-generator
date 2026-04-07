# -*- coding: utf-8 -*-
import config
import requests
import json
import os
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


print('> start')

def parse_rss(xml_content):
    """解析 RSS XML 内容并转换为字典"""
    root = ET.fromstring(xml_content)
    
    # 处理命名空间
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'atom': 'http://www.w3.org/2005/Atom',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    
    channel = root.find('channel')
    if channel is None:
        # 可能是 Atom 格式
        return parse_atom(root)
    
    # RSS 2.0 格式
    rss_data = {
        'title': get_text(channel, 'title'),
        'link': get_text(channel, 'link'),
        'description': get_text(channel, 'description'),
        'lastBuildDate': get_text(channel, 'lastBuildDate'),
        'items': []
    }
    
    for item in channel.findall('item'):
        item_data = {
            'title': get_text(item, 'title'),
            'link': get_text(item, 'link'),
            'description': get_text(item, 'description'),
            'pubDate': get_text(item, 'pubDate'),
            'guid': get_text(item, 'guid')
        }
        rss_data['items'].append(item_data)
    
    return rss_data

def parse_atom(root):
    """解析 Atom 格式"""
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    rss_data = {
        'title': get_text_atom(root, 'atom:title', ns),
        'link': '',
        'description': '',
        'lastBuildDate': get_text_atom(root, 'atom:updated', ns),
        'items': []
    }
    
    # 获取 link
    link_elem = root.find('atom:link', ns)
    if link_elem is not None:
        rss_data['link'] = link_elem.get('href', '')
    
    for entry in root.findall('atom:entry', ns):
        item_data = {
            'title': get_text_atom(entry, 'atom:title', ns),
            'link': '',
            'description': get_text_atom(entry, 'atom:summary', ns) or get_text_atom(entry, 'atom:content', ns),
            'pubDate': get_text_atom(entry, 'atom:published', ns) or get_text_atom(entry, 'atom:updated', ns),
            'guid': get_text_atom(entry, 'atom:id', ns)
        }
        # 获取 entry 的 link
        entry_link = entry.find('atom:link', ns)
        if entry_link is not None:
            item_data['link'] = entry_link.get('href', '')
        
        rss_data['items'].append(item_data)
    
    return rss_data

def get_text(element, tag, default=''):
    """获取子元素的文本内容"""
    elem = element.find(tag)
    return elem.text if elem is not None else default

def get_text_atom(element, tag, namespaces, default=''):
    """获取 Atom 命名空间下的子元素文本内容"""
    elem = element.find(tag, namespaces)
    return elem.text if elem is not None else default

def save_json(name, content):
    root = 'v2'
    dir_path = os.path.join(root, name)
    file_path = os.path.join(dir_path, 'data.json')
    
    # 创建路径
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f'> saved: {file_path}')

def generate_filename(url):
    """从 URL 生成文件名"""
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    # 替换特殊字符
    filename = path.replace('/', '_').replace(':', '_')
    return filename or 'rss_feed'

try:
    links = config.read('links')
    print('> links: ', links)
    
    for link in links:
        print('> fetching: ', link)
        try:
            response = requests.get(link, timeout=30)
            response.raise_for_status()
            
            # 解析 RSS
            rss_data = parse_rss(response.content)
            rss_data['feed_url'] = link
            rss_data['fetch_time'] = requests.get('https://api.github.com').headers.get('Date', '')
            
            # 生成文件名
            filename = generate_filename(link)
            save_json(filename, rss_data)
            
        except Exception as e:
            print(f'> error fetching {link}: {e}')
            continue

except Exception as e:
    print('> exception: ', e)

print('> end')
