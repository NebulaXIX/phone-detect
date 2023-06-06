import os
import json
import codecs
import shutil
import xml.etree.ElementTree as ET
import os
from PIL import Image


def easydata_to_voc(dataroot):
    files = os.listdir(dataroot)

    os.mkdir(dataroot + '/images')
    os.mkdir(dataroot + '/annotations')
    os.mkdir(dataroot + '/jsons')
    os.mkdir(dataroot+"/labels")
    images_path = os.path.join(dataroot, 'images')
    annotations_path = os.path.join(dataroot, 'annotations')
    jsons_path = os.path.join(dataroot, 'jsons')

    for file in files:
        if file.endswith('.json'):
            shutil.move(os.path.join(dataroot, file), jsons_path)
        if file.endswith('.jpeg'):
            shutil.move(os.path.join(dataroot, file), images_path)

    json_files = os.listdir(jsons_path)
    for json_file in json_files:
        file_id = json_file.replace("." + json_file.split(".")[len(json_file.split('.')) - 1], "")
        img = os.path.join(dataroot + "\\images", file_id + ".jpeg")
        size = Image.open(img)
        json_path = os.path.join(jsons_path, json_file)
        names, xmins, ymins, xmaxs, ymaxs = [], [], [], [], []
        height, width = 0, 0
        with open(json_path, 'r', encoding='utf-8') as f:
            json_file
            set = json.load(f)
            result = set['labels']
            num = len(result)
            for n in range(num):
                dict = result[n]
                name = dict['name']
                xmin = dict['x1']
                ymin = dict['y1']
                xmax = dict['x2']
                ymax = dict['y2']

                names.append(name)
                xmins.append(xmin)
                ymins.append(ymin)
                xmaxs.append(xmax)
                ymaxs.append(ymax)

            # print(names, xmins, ymins, xmaxs, ymaxs, height, width)
        xml_path = os.path.join(annotations_path, file_id + '.xml')

        xml = codecs.open(xml_path, 'w', encoding='utf-8')
        xml.write('<annotation>')
        xml.write('<folder>' + 'VOC2007' + '</folder>')
        xml.write('<filename>' + file_id + '.jpeg</filename>')  # 1.jpeg
        xml.write('<size>')
        xml.write('<width>' + str(size.width) + '</width>')
        xml.write('<height>' + str(size.height) + '</height>')
        xml.write('<depth>3</depth>')
        xml.write('</size>')
        xml.write('<segmented>0</segmented>')

        for i in range(len(names)):
            xml.write('<object>')
            xml.write('<name>' + "phone" + '</name>')
            xml.write('<bndbox>')
            xml.write('<xmin>' + str(xmins[i]) + '</xmin>')
            xml.write('<ymin>' + str(ymins[i]) + '</ymin>')
            xml.write('<xmax>' + str(xmaxs[i]) + '</xmax>')
            xml.write('<ymax>' + str(ymaxs[i]) + '</ymax>')
            xml.write('</bndbox>')
            xml.write('</object>')

        xml.write('</annotation>')


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(xml_file, class_id, voc_folder, yolo_folder):
    file_name = xml_file.strip(".xml")  # 这一步将所有voc格式标注文件取出后缀名“.xml”，方便接下来作为yolo格式标注文件的名称
    in_file = open(os.path.join(voc_folder, xml_file))  # 打开当前转换的voc标注文件
    out_file = open(os.path.join(yolo_folder, file_name + ".txt", ), 'w')  # 创建并打开要转换成的yolo格式标注文件
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        cls_id = class_id.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text),
             float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def voc_to_yolo(voc_folder, yolo_folder, class_id):
    xml_file_list = os.listdir(voc_folder)
    for xml_file in xml_file_list:
        convert_annotation(xml_file, class_id, voc_folder, yolo_folder)


if __name__ == '__main__':
    DATAROOT = 'C:\\Users\\msi\\Desktop\\手机验证集V2\\1854179_99_1686024983'
    easydata_to_voc(DATAROOT)
    voc_to_yolo(DATAROOT + '\\annotations',
                DATAROOT + '\\labels', ['phone'])
