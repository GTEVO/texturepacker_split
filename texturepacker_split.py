#!python v2.7 encode format : Western(ISO 8859-15)
# 1?   ?? PIL
# 2?   ??png?plist?????
import os,sys
from xml.etree import ElementTree
from PIL import Image

def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d

def gen_png_from_plist(plist_filename, png_filename):
    file_path = plist_filename.replace('.plist', '')
    big_image = Image.open(png_filename)
    root = ElementTree.fromstring(open(plist_filename, 'r').read())
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():
        # ?????? Rect
        rectlist = to_list(v['frame'])
        rect_w = rectlist[2]
        rect_h = rectlist[3]
        is_rotated = v['rotated']
        if is_rotated:
            rect_w = rectlist[3]
            rect_h = rectlist[2]
        rect_w = int(rect_w)
        rect_h = int(rect_h)
        rect = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + rect_w,
            int(rectlist[1]) + rect_h,
            )
        # ?????? ??
        rect_on_big = big_image.crop(rect)
        if is_rotated:
            # ?????????....
            side_length = max(rect_w, rect_h)
            temp_image = Image.new('RGBA',(side_length, side_length),(0,0,0,0))
            temp_x = side_length / 2 - rect_w / 2
            temp_y = side_length / 2 - rect_h / 2
            temp_rect = (
                temp_x,
                temp_y,
                temp_x + rect_w,
                temp_y + rect_h
            )
            temp_image.paste(rect_on_big, temp_rect, mask=0)
            rect_on_big = temp_image.rotate(90)
            temp_box_x = side_length / 2 - rect_h / 2
            temp_box_y = side_length / 2 - rect_w / 2
            temp_box = (
                temp_box_x,
                temp_box_y,
                temp_box_x + rect_h,
                temp_box_y + rect_w
            )
            rect_on_big = rect_on_big.crop(temp_box)

        # ?????
        sizelist = [ int(x) for x in to_list(v['sourceSize'])]
        result_image = Image.new('RGBA', sizelist, (0,0,0,0))
        
        # ?????
        source_color_rect = to_list(v['sourceColorRect'])
        result_rect = (
            int(source_color_rect[0]),
            int(source_color_rect[1]),
            int(source_color_rect[0]) + int(source_color_rect[2]),
            int(source_color_rect[1]) + int(source_color_rect[3])
        )
        #print k
        #print 'rotated:', is_rotated
        #print 'original img:', result_image
        #print 'broken rect in sprite atlas:', rect
        #print 'broken rect in original img:', result_rect
        #print 'broken img:', rect_on_big
        result_image.paste(rect_on_big, result_rect, mask=0)

        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        outfile = (file_path+'/' + k).replace('gift_', '')
        #print outfile, "generated succeessfully"
        #print '------------------------------------------------------------------------------------'
        result_image.save(outfile)

if __name__ == '__main__':
    curexecDir = os.getcwd()
    for root,dirs,files in os.walk(curexecDir):
        for filename in files:
            if os.path.splitext(filename)[1] == '.plist':
                name = os.path.splitext(filename)[0]
                plist_filename = filename 
                png_filename = name + '.pvr.png'
                print 'Start To Split Png :' + png_filename
                if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
                    gen_png_from_plist( plist_filename, png_filename )
                else:
                    print "make sure you have boith plist and png files in the same directory"
        