import os

from objectmapper import ObjectMapper
from reader import Reader


class Transformer(object):
    def __init__(self, xml_dir, out_dir, class_file):
        self.xml_dir = xml_dir
        self.out_dir = out_dir
        self.class_file = class_file

    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        xml_files = reader.get_xml_files()
        classes = reader.get_classes(self.class_file)
        object_mapper = ObjectMapper()
        annotations = object_mapper.bind_files(xml_files, xml_dir=self.xml_dir)
        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename))
            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))
            with open(output_path, "w+") as f:
                f.write(self.to_darknet_format(annotation, classes))

    def to_darknet_format(self, annotation, classes):
        result = []
        for obj in annotation.objects:
            if obj.name not in classes:
                print("Please, add '%s' to classes.txt file." % obj.name)
                exit()
            x, y, width, height = self.get_object_params(obj, annotation.size)
            result.append("%d %.6f %.6f %.6f %.6f" % (classes[obj.name], x, y, width, height))
        return "\n".join(result)

    @staticmethod
    def get_object_params(obj, size):

        #if it has invalid height or width
        if size.width==0 or size.height==0:
          print(Invalid image height or width)
          return -1, -1, -1, -1
        
        
        box = obj.box
        x_min=int( float(box.xmin))
        x_max=int( float(box.xmax))
        y_min=int( float(box.ymin))
        y_max=int( float(box.ymax))


        absolute_x = x_min + 0.5 * (x_max - x_min)
        absolute_y = y_min + 0.5 * (y_max - y_min)

        absolute_width = x_max - x_min
        absolute_height = y_max - y_min

        x = absolute_x / size.width
        y = absolute_y / size.height
        width = absolute_width / size.width
        height = absolute_height / size.height

        return x, y, width, height

    @staticmethod
    def darknet_filename_format(filename):
        pre, ext = os.path.splitext(filename)
        return "%s.txt" % pre
