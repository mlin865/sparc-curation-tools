# VERSION = sparc.curation.tools.__version__

SCAFFOLD_DIR_MIME = 'inode/vnd.abi.scaffold+directory'
SCAFFOLD_FILE_MIME = 'application/x.vnd.abi.scaffold.meta+json'
SCAFFOLD_VIEW_MIME = 'application/x.vnd.abi.scaffold.view+json'
SCAFFOLD_THUMBNAIL_MIME = 'image/x.vnd.abi.scaffold.thumbnail+jpeg'
CONTEXT_INFO_MIME = 'application/x.vnd.abi.context-information+json'
TARGET_MIMES = [SCAFFOLD_DIR_MIME, SCAFFOLD_FILE_MIME, SCAFFOLD_THUMBNAIL_MIME]

SIZE_NAME = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")

FILENAME_COLUMN = 'filename'
ADDITIONAL_TYPES_COLUMN = 'additional types'
MANIFEST_DIR_COLUMN = 'manifest_dir'
SOURCE_OF_COLUMN = 'isSourceOf'
DERIVED_FROM_COLUMN = 'isDerivedFrom'
FILE_LOCATION_COLUMN = 'file_location'
SUPPLEMENTAL_JSON_COLUMN = 'Supplemental JSON Metadata'
ANATOMICAL_ENTITY_COLUMN = 'isAboutAnatomicalEntity'

SCAFFOLD_DIR = "files\derivative\Scaffold"

MIMETYPE_TO_FILETYPE_MAP = {
    SCAFFOLD_FILE_MIME: 'Metadata',
    SCAFFOLD_VIEW_MIME: 'View',
    SCAFFOLD_THUMBNAIL_MIME: 'Thumbnail',
    SCAFFOLD_DIR_MIME: 'Directory'
}

MIMETYPE_TO_PARENT_FILETYPE_MAP = {
    SCAFFOLD_VIEW_MIME: 'Metadata',
    SCAFFOLD_THUMBNAIL_MIME: 'View'
}

MIMETYPE_TO_CHILDREN_FILETYPE_MAP = {
    SCAFFOLD_VIEW_MIME: 'Thumbnail',
    SCAFFOLD_FILE_MIME: 'View'
}