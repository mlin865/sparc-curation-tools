import os
from pathlib import Path

import pandas as pd
from sparc.curation.tools.annotations.scaffold import ScaffoldAnnotation, IncorrectAnnotationError, NotAnnotatedError, NoViewError, NoDerivedFromError, NoThumbnailError

from sparc.curation.tools.base import Singleton
from sparc.curation.tools.definitions import FILE_LOCATION_COLUMN, FILENAME_COLUMN, ADDITIONAL_TYPES_COLUMN, SCAFFOLD_FILE_MIME, SCAFFOLD_VIEW_MIME, SCAFFOLD_THUMBNAIL_MIME


class ManifestDataFrame(metaclass=Singleton):
    # dataFrame_dir = ""
    _manifestDataFrame = None
    _scaffold_data = None

    def setup_dataframe(self, dataset_dir):
        self.read_manifest(dataset_dir)
        self.setup_data()
        return self

    def read_manifest(self, dataset_dir):
        # self._annotatedFileList = None
        # self._realScaffoldList = None
        # self.dataFrame_dir = dataset_dir
        result = list(Path(dataset_dir).rglob("manifest.xlsx"))
        self._manifestDataFrame = pd.DataFrame()
        for r in result:
            xl_file = pd.ExcelFile(r)
            # print(xl_file)
            for sheet_name in xl_file.sheet_names:
                currentDataFrame = xl_file.parse(sheet_name)
                currentDataFrame['sheet_name'] = sheet_name
                currentDataFrame['manifest_dir'] = os.path.dirname(r)
                self._manifestDataFrame = pd.concat([currentDataFrame, self._manifestDataFrame])
        # print(manifestDataFrame)
        self._manifestDataFrame[FILE_LOCATION_COLUMN] = self._manifestDataFrame.apply(
            lambda row: os.path.join(row['manifest_dir'], row[FILENAME_COLUMN]) if pd.notnull(row[FILENAME_COLUMN]) else None, axis=1)
        return self._manifestDataFrame

    def get_manifest(self):
        return self._manifestDataFrame

    def setup_data(self):
        self._scaffold_data = ManifestDataFrame.Scaffold()
        self._scaffold_data.set_scaffold_annotations(
            [ScaffoldAnnotation(row) for i, row in self._manifestDataFrame[self._manifestDataFrame[ADDITIONAL_TYPES_COLUMN].notnull()].iterrows()]
        )
        self._scaffold_data.set_scaffold_locations([i.get_location() for i in self._scaffold_data.get_scaffold_annotations()])

    def get_scaffold_data(self):
        return self._scaffold_data

    class Scaffold(object):
        _data = {
            'annotations': [],
            'locations': [],
        }

        def set_scaffold_annotations(self, annotations):
            self._data['annotations'] = annotations

        def get_scaffold_annotations(self):
            return self._data['annotations']

        def set_scaffold_locations(self, locations):
            self._data['locations'] = locations

        def get_scaffold_locations(self):
            return self._data['locations']

        def get_incorrect_annotations(self, on_disk):
            errors = []

            on_disk_metadata_files = on_disk.get_scaffold_data().get_metadata_files()
            on_disk_view_files = on_disk.get_scaffold_data().get_view_files()
            on_disk_thumbnail_files = on_disk.get_scaffold_data().get_thumbnail_files()

            for i in self._data['annotations']:
                if i.get_additional_type() == SCAFFOLD_FILE_MIME:
                    if i.get_location() not in on_disk_metadata_files:
                        errors.append(IncorrectAnnotationError(i.get_location(), i.get_additional_type()))

                if i.get_additional_type() == SCAFFOLD_VIEW_MIME:
                    if i.get_location() not in on_disk_view_files:
                        errors.append(IncorrectAnnotationError(i.get_location(), i.get_additional_type()))

                if i.get_additional_type() == SCAFFOLD_THUMBNAIL_MIME:
                    if i.get_location() not in on_disk_thumbnail_files:
                        errors.append(IncorrectAnnotationError(i.get_location(), i.get_additional_type()))
            return errors

        def get_missing_annotations(self, on_disk):
            errors = []

            on_disk_metadata_files = on_disk.get_scaffold_data().get_metadata_files()
            on_disk_view_files = on_disk.get_scaffold_data().get_view_files()
            on_disk_thumbnail_files = on_disk.get_scaffold_data().get_thumbnail_files()

            for i in on_disk_metadata_files:
                if i not in self._data['locations']:
                    errors.append(NotAnnotatedError(i, SCAFFOLD_FILE_MIME))

            print('get missing annotations')
            for i in on_disk_view_files:
                if i not in self._data['locations']:
                    print('append error')
                    print(i)
                    errors.append(NotAnnotatedError(i, SCAFFOLD_VIEW_MIME))

            for i in on_disk_thumbnail_files:
                if i not in self._data['locations']:
                    errors.append(NotAnnotatedError(i, SCAFFOLD_THUMBNAIL_MIME))

            return errors

        def get_scaffold_no_view(self, on_disk):
            errors = []

            on_disk_metadata_files = on_disk.get_scaffold_data().get_metadata_files()

            for i in self._data['annotations']:
                if i.get_location() in on_disk_metadata_files and not i.get_children():
                    errors.append(NoViewError(i.get_location()))
            return errors

        def get_view_no_scaffold(self, on_disk):
            errors = []
            on_disk_view_files = on_disk.get_scaffold_data().get_view_files()
            for i in self._data['annotations']:
                if i.get_location() in on_disk_view_files and not i.get_parent():
                    errors.append(NoDerivedFromError(i.get_location(), SCAFFOLD_VIEW_MIME))
            return errors

        def get_view_no_thumbnail(self, on_disk):
            result = []
            on_disk_view_files = on_disk.get_scaffold_data().get_view_files()
            for i in self._data['annotations']:
                if i.get_location() in on_disk_view_files and not i.get_children():
                    result.append(NoThumbnailError(i.get_location()))
            return result

        def get_thumbnail_no_view(self, on_disk):
            result = []
            on_disk_thumbnail_files = on_disk.get_scaffold_data().get_thumbnail_files()
            for i in self._data['annotations']:
                if i.get_location() in on_disk_thumbnail_files and not i.get_parent():
                    result.append(NoDerivedFromError(i.get_location(), SCAFFOLD_THUMBNAIL_MIME))
            return result
    # def get_real_scaffold(self):
    #     # Return a Series of filename
    #     return [os.path.basename(location) for location in self._realScaffoldList]
    #
    # def get_annotated_scaffold(self):
    #     result = []
    #     for i in self._annotatedFileList:
    #         if i._additionalType == SCAFFOLD_FILE_MIME:
    #             result.append(i)
    #     return result
    #
    # def get_annotated_view(self):
    #     result = []
    #     for i in self._annotatedFileList:
    #         if i._additionalType == SCAFFOLD_VIEW_MIME:
    #             result.append(i)
    #     return result
    #
