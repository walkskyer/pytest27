# -*- coding:gbk -*-
__author__ = 'walkskyer'
"""
下载整个网页资源文件及结构
移植自php脚本
20150214
"""
import re
import urllib2
import os
from urlparse import urlparse
import socket
import sys, getopt
import time

socket.setdefaulttimeout(30)
target_root_dir = 'html'

pattern = {
    'js': re.compile(r'<script.*?src=[\'\"](.*?)[\'\"].*?</script>', re.IGNORECASE),
    'css': re.compile(r'<link.*?href=[\'\"](.*?)[\'\"].*?>', re.IGNORECASE),
    'page_image': re.compile(r'<img.*?src=[\'\"](.*?)[\'\"].*?>', re.IGNORECASE),
    'css_image': re.compile(r'url\([\'\"]?(.*?)[\'\"]?\)', re.IGNORECASE),
}
dirs = {'js': 'js',
        'css': 'css',
        'page_image': 'images_page',
        'css_image': 'images',
        'font': 'fonts',
        'inner_css': '../images',
        'inner_font': '../fonts',
        'inner_import_css': '.',
}
font_ext = ('.ttf', '.eot', '.svg', '.woff', '.woff2')

inner_files = {'css': {'pattern': re.compile('url\([\'\"]?(.*?)[\'\"]?\)', re.IGNORECASE), 'dir': '../images'}}

# 是否使用原始文件名保存文件，如果否将在网页中的路径转换成文件名保存。
on_save_basename = True


def wk_target_name(v, origin_name=True):
    """
    获取文件名
    :param v:
    :param origin_name:
    :return:
    """
    filename = os.path.basename(v.strip())

    pos = filename.find('?')
    if pos != -1:
        filename = filename[0: pos]

    if filename and not origin_name:
        path = os.path.dirname(v.strip()).replace('http://', '').replace('https://', '').replace('//', '').replace('..', '')
        filename = '%s-%s' % (path.replace('/', '-'), filename)
    return filename


def real_url(uri, base_url=''):
    """
    返回真实的url
    :param uri:
    :param base_url:
    :return:
    """
    try:
        if uri.find('http://') == 0 or uri.find('https://') == 0:
            return uri
        if uri.startswith('//'):
            return 'http:%s' % uri

        url_info = urlparse(base_url)
        root_path = '%s://%s' % (url_info.scheme, url_info.netloc)

        if uri == '.' or not uri:
            uri = base_url
        elif uri[0] == '/':
            uri = root_path + uri
        else:
            uri = base_url + '/' + uri
        return uri
    except Exception, e:
        # charset error try again
        print e
        if not isinstance(uri,'unicode'):
            return real_url(getCodeStr(uri,'utf-8').decode('utf-8'), base_url)

    try:
        if uri == '.' or not uri:
            uri = base_url
        elif uri[0] == '/':
            uri = root_path + uri
        else:
            uri = base_url + '/' + uri
    except Exception, e:
        log(e)
        return real_url(getCodeStr(uri, 'utf-8').decode('utf-8'), base_url)
    return uri


def download_files(file_list, dir, base_url='', origin_name=True):
    """
    下载文件列表
    :param file_list:
    :param dir:
    :param base_url:
    :param origin_name:
    :return:
    """
    if not os.path.isdir(target_root_dir+'/'+dir):
        print 'curr dir: %s and I will make dir： %s\n' % (os.getcwd(), target_root_dir+'/'+dir)
        os.mkdir(target_root_dir+'/'+dir)

    for v in file_list:
        filename = wk_target_name(v.strip(), origin_name)
        if filename == '':
            continue

        print "%s_filename:%s\n" % (dir, filename)
        if is_font_file(filename):
            download_file(dirs['font'] + '/' + filename, v, base_url)
            continue
        if filename.endswith('.css'):
            download_file(dirs['css'] + '/' + filename, v, base_url)
            continue
        download_file(dir + '/' + filename, v, base_url)


def download_file(filename, target_url, base_url=''):
    """
    下载文件0
    :param filename:
    :param target_url:
    :param base_url:
    :return:
    """

    filename = target_root_dir + '/' + filename
    if not os.path.isdir(os.path.dirname(filename)):
        print 'curr dir: %s and I will make dir： %s\n' % (os.getcwd(), dir)
        os.mkdir(os.path.dirname(filename))

    if os.path.isfile(filename):
        print 'File: %s is exist.' % filename
        return

    if target_url.strip().startswith('data:image'):
        print 'URL seems not a file: %s .' % filename
        return ''

    target_url = target_url.strip().replace('\'', '').replace('"', '')
    target_url = real_url(target_url, base_url)

    if not target_url:
        return

    print "download: %s \n" % target_url
    file_put_contents(filename, file_get_contents(target_url))


def file_put_contents(filename, content, mode='wb'):
    """
    write something to a file
    :param filename:
    :param content:
    :return:
    """
    if content is None:
        return
    try:
        f = open(getCodeStr(filename), mode)
        f.write(content)
        f.close()
    except IOError, e:
        print e


def file_get_contents(url):
    """
    read the file content
    :param url:
    :return:
    """
    if url.find('http://') != -1 or url.find('https://') != -1:
        try:
            req = urllib2.Request(url,None,{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0'})
            return urllib2.urlopen(req).read()
            #return urllib.urlopen(url).read()
        except Exception, e:
            msg = u'下载文件 %s 时报出错误: %s' % (url, e)
            print "file %s download error: %s" % (url, e)
            log(msg)
            return None

    if not os.path.isfile(url):
        url = target_root_dir + '/' + url
    if not os.path.isfile(url):
        return
    f = open(url, 'rb')
    content = f.read()
    f.close()
    return content


def is_font_file(filename):
    """
    根据文件名判断是否为字体文件
    :param filename:
    :return:
    """
    filename = wk_target_name(filename.strip().lower())
    last_dot_index = filename.rfind('.')
    if last_dot_index > -1:
        if filename[last_dot_index:] in font_ext:
            return True
    return False


def log(msg, log_file='download'):
    if msg is None:
        return
    if isinstance(msg, unicode):
        msg = msg.encode('utf-8', 'ignore')

    return file_put_contents(target_root_dir + '/' + '%s.log' % log_file, "[%s] %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg), 'ab')


def replace_resource_path(matchObj, target_dir='', origin_name=True):
    """
    替换资源文件目录
    :param matchObj:
    :param target_dir:
    :return:
    """
    match = matchObj.group(1).strip()
    if not match:
        return ''

    if match.startswith('data:image'):
        return matchObj.group(0)

    if is_font_file(match):
        if target_dir.startswith('..'):
            target_dir = dirs['inner_font']
        else:
            target_dir = dirs['font']

    if match.endswith('.css') and target_dir.startswith('..'):
            target_dir = dirs['inner_import_css']

    return matchObj.group(0).replace(match, target_dir + '/' + wk_target_name(match, origin_name))


def replace_inner_source_file_path(matchObj):
    return replace_resource_path(matchObj, inner_files['css']['dir'], on_save_basename)

# convert encoding
def getCodeStr(result, target_charset='utf-8'):
    #gb2312
    try:
        myResult = result.decode('gb2312').encode(target_charset, 'ignore')
        return myResult
    except:
        pass
        #utf-8
    try:
        myResult = result.decode('utf-8').encode(target_charset, 'ignore')
        return myResult
    except:
        pass

    #unicode
    try:
        myResult = result.encode(target_charset, 'ignore')
        return myResult
    except:
        pass
        #gbk
    try:
        myResult = result.decode('gbk').encode(target_charset, 'ignore')
        return myResult
    except:
        pass
        #big5
    try:
        myResult = result.decode('big5').encode(target_charset, 'ignore')
        return myResult
    except:
        pass


def run_download(url, base_url, base_name):
    if not os.path.isdir(target_root_dir):
        os.mkdir(target_root_dir)
    #os.chdir(target_root_dir)

    page_content = file_get_contents(url)

    content = file_get_contents(url)
    for k, v in pattern.items():
        files1 = v.findall(content)
        print files1
        if not files1:
            continue

        # link 不一定是css
        if k == 'css':
            filesTemp= []
            for tFilename in files1:
                if wk_target_name(tFilename.strip()).endswith('.css'):
                    filesTemp.append(tFilename)
            print 'Css Files:',  filesTemp
            files1 = filesTemp

        if on_save_basename:
            save_basename = not (k == 'page_image')
        else:
            save_basename = on_save_basename

        download_files(files1, dirs[k], base_url, save_basename)

        def replace_source_file_path(matchObj):
            """
            替换
            :param matchObj:
            :return:
            """
            return replace_resource_path(matchObj, dirs[k], save_basename)
            # match = matchObj.group(1)
            # if not match:
            #     return ''
            # if match.strip().startswith('data:image/'):
            #     return matchObj.group(0)
            #
            # return matchObj.group(0).replace(match, dirs[k] + '/' + wk_target_name(match, save_basename))
        # return str_replace(match[1],dirs[k].'/'.wk_basename(match[1]),match[0])
        page_content = v.sub(replace_source_file_path, page_content)

        if k == 'css':  # 如果是css 还要下载css中引用的文件
            for css_file in files1:
                if not css_file.endswith('.css'):
                    continue
                print 'css/' + wk_target_name(css_file)
                css_content = file_get_contents('css/' + wk_target_name(css_file, save_basename))
                if css_content is None:
                    continue
                css_matches = inner_files['css']['pattern'].findall(css_content)
                if css_matches:
                    download_files(css_matches, dirs['css_image'], real_url(os.path.dirname(css_file), base_url), save_basename)
                    css_content = inner_files['css']['pattern'].sub(replace_inner_source_file_path, css_content)
                    file_put_contents(target_root_dir + '/' + 'css/' + wk_target_name(css_file, save_basename), css_content)

    file_put_contents(target_root_dir + '/' +base_name, page_content)
    print "Download task is complete ^_^"
    print "*********************************************************************************************************"
    print os.getcwd()
    #os.chdir('..')
    print os.getcwd()

def usage():
    print 'This tools is used to download one page from the online web site to your local host.It will download the page struct ,js,css And images.And powered by walkskyer ^_^'
    print "usage:"
    print "-u --url: target url"
    print "-t --target-name: save the page as target name"
    sys.exit()

if __name__ == "__main__":
    # url = 'http://www.273.cn/mobile'

    url = base_url = ''
    target_name = 'index.html'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:t:b:l=", ["url=", "target-name=", "base-url=", "local-file="])
    except getopt.GetoptError:
        usage()

    if not len(opts):
        usage()

    for opt, argv in opts:
        if opt in ("-h"):
            usage()
        if opt in ("-u", "--url"):
            url = argv
        if opt in ("-t", "--target-name"):
            target_name = argv
        if opt in ("-b", "--base-url"):
            base_url = argv
        if opt in ("-l", "--local-file"):
            url, base_url = argv, url
    """
        if len(sys.argv) <= 1:
            while len(url) <= 0:
                url = raw_input('please input a url(*):')
    
        if len(sys.argv) <= 2:
            target_name = raw_input('please input the target name (optional default:index.html):')
    """
    if os.path.isfile(getCodeStr(url)):
        """while len(base_url) <= 0:
            base_url = raw_input('please input the resource root url (To locate the images,css or js file in this html file):')"""

        if base_url.find(r'://') == -1:
            base_url = 'http://%s' % base_url

        url_info = urlparse(base_url)
        base_name = os.path.basename(url)
        url = getCodeStr(url)
    else:
        if url.find(r'://') == -1:
            url = 'http://%s' % url
        url_info = urlparse(url)
        base_url = os.path.dirname(url)
        base_name = os.path.basename(url)

        pos = int(base_name.find('.'))
        if pos is -1:
            ext = None
        else:
            ext = base_name[pos + 1:]
        if ext not in ('html', 'htm', 'php', 'asp', 'jsp', 'aspx'):
            base_url = url[0:url.rfind('/')]
            base_name = 'index.html'

    root_path = '%s://%s' % (url_info.scheme, url_info.netloc)

    if base_url == 'http:' or base_url == 'http:/':
        base_url = root_path

    if target_name:
        base_name = target_name

    print 'We will download the page use this url:%s' % getCodeStr(url,'utf-8')
    time.sleep(2)

    run_download(url,base_url,base_name)
