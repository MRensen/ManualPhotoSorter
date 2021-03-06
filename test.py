import unittest
from main import *


class TestSave(unittest.TestCase):

    def test_save(self):
        app = GUI()
        app.import_from_folder = "/home/mark/Pictures"
        app.get_photos()
        app.platform = "linux"
        app.base_path = "/home/mark"
        app.home_path = "/home/mark/Pictures/PhotoSorter"
        app.buttonHeightOffset = 30
        app.h = 700
        app.w = 700
        FB = root.FolderButton(app, "test", "/home/mark/Pictures/PhotoSorter")
        app.folderButton_list = [FB]
        #TODO: update this dict so that it conatins the expected results of app.save()
        result = {#"photos": photos,
                "photo_counter": app.photo_counter,
                #"folderButton_list": folderButton_list,
                "platform": app.platform,
                "base_path": app.base_path,
                "home_path": app.home_path,
                "importFolder": app.import_from_folder,
                "buttonHeigthOffset": app.buttonHeightOffset,
                "w": app.w,
                "h": app.h
                }
        self.assertEqual(app.save(), result, "dict should be as is")

if __name__ == "__main__":
    unittest.main()

