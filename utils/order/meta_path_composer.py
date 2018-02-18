import re
import logging
from datetime import datetime
import os


def get_author(metadata,  file_full_path):
    author = ""
    try:
        text = metadata.exportPlaintext()
    except AttributeError:
        text = ""
    text = str(text) if isinstance(text, list) else text
    if re.search(
            u".*author.*", text, re.IGNORECASE
    ):
        author = u"author_"
        try:
            author += metadata._Metadata__data["author"].values[0].value
        # "/"+"author"
        except (IndexError, KeyError, AttributeError):
            pass
        except Exception as e:
            logging.debug("No author available")
            logging.exception(e)
    logging.debug("author " + author)
    return author


def get_album(metadata, file_full_path):
    album = u""
    try:
        text = metadata.exportPlaintext()
    except AttributeError:
        text = ""
    text = str(text) if isinstance(text,list) else text
    if re.search(
            u".*album.*", text, re.IGNORECASE
    ):
        album = "album_"
        try:
            album += metadata._Metadata__data["album"].values[0].value
        # "/"+"album"
        except (IndexError, KeyError, AttributeError):
            pass
        except Exception as e:
            logging.debug("No album available")
            logging.exception(e)
    logging.debug("album " + album)
    return album


def get_camera(metadata, file_full_path):
    camera_model = ""
    try:
        if "Model" in metadata.EXIF_KEY:
            camera_model = "camera_"
            camera_model += metadata._Metadata__data["camera_model"].values[0].value
    # "/"+"camera"
    except (IndexError, KeyError, AttributeError):
        pass
    except Exception as e:
        logging.debug("No camera model available")
        logging.exception(e)
    logging.debug("camera " + camera_model)
    return camera_model


def get_whatsapp(metadata, file_full_path):
    whatsapp_path = ""
    try:
        if re.search(
                ".*whatsapp.*", file_full_path, re.IGNORECASE
        ):
            whatsapp_path = "whatsapp"
        logging.debug("whatsapp " + whatsapp_path)
    except (IndexError, KeyError, AttributeError):
        pass
    except Exception as e:
        logging.exception(e)
    return whatsapp_path


def get_date(metadata, file_full_path):
    date_str = "sinkDateNotfound"
    try:
        text = metadata.exportPlaintext()
    except AttributeError:
        text = ""
    text = str(text) if isinstance(text, list) else text
    if re.search(u".*date.*", text, re.IGNORECASE):
        try:
            date_str = metadata._Metadata__data["creation_date"].values[0].value.strftime("%y_%m_%d")
        except (KeyError, IndexError) as e:
            try:
                date_str = metadata._Metadata__data["last_modification"].values[0].value.strftime("%y_%m_%d")
            except (KeyError, IndexError) as e:
                try:
                    logging.debug(
                        "key not found in metadata " + file_full_path + ":" + str(
                            metadata._Metadata__data.keys()
                        )
                    )
                    logging.debug(text)
                except (IndexError, KeyError, AttributeError):
                    pass
                except Exception as e:
                    logging.exception(e)
    if date_str == "sinkDateNotfound":
        try:
            fname = file_full_path.split("/")[-1]
            date_from_fname = re.search(
                u"[a-z]*.([0-9]{8}).*", fname, re.IGNORECASE
            )
            if date_from_fname:
                logging.debug("Trying to get date from filename")
                year = int(date_from_fname.group(1)[0:4])
                month = int(date_from_fname.group(1)[4:6])
                day = int(date_from_fname.group(1)[6:8])
                date_str = datetime(year, month, day).strftime("%y_%m_%d")
        except (IndexError, UnicodeDecodeError, ValueError) as e:
            pass
    logging.debug("date " + date_str)
    return date_str


THRESHOLD_H = 600
THRESHOLD_W = 800


def get_icon(metadata,  file_full_path):
    icon_path = ""
    try:
        if metadata:
            width = metadata._Metadata__data["width"].values[0].value
            height = metadata._Metadata__data["height"].values[0].value
            if width < THRESHOLD_W or height < THRESHOLD_H:
                icon_path = "Icons"
        else:
            if os.path.getsize(file_full_path) < 100 * 1000:
                icon_path = "Icons"
    except (IndexError, KeyError, AttributeError):
        pass
    except Exception as e:
        logging.exception(e)
    return icon_path


path_update_map = {
    "image/*": [get_camera, get_whatsapp, get_icon, get_date],
    "audio/*": [get_author, get_album]
}


def run_path_update(mime_type, metadata,  file_full_path, file_ordered_path):
    for key_regex, path_updaters in path_update_map.items():
        try:
            if re.search(key_regex, mime_type):
                for updater in path_updaters:
                    path_update = updater(
                        metadata, file_full_path
                    )
                    if path_update:
                        file_ordered_path = os.path.join(
                            file_ordered_path, path_update
                        )
        except TypeError:
            file_ordered_path = os.path.join(file_ordered_path, "sinkNoPathUpdate")
    return file_ordered_path
