import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from loguru import logger

from lrutility.logger import configure_loguru
from lrutility.XMPDataclass import (
    CameraRawSettings,
    DublinCoreInfo,
    DynamicMediaInfo,
    ExifInfo,
    FlashInfo,
    LensInfo,
    PhotoshopInfo,
    TiffInfo,
    XmpBasicInfo,
    XmpDocumentInfo,
    XMPMetadata,
)


class XMPParser:
    """XMPファイルをパースしてメタデータを抽出するクラス。"""

    NAMESPACES = {
        "x": "adobe:ns:meta/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "xmp": "http://ns.adobe.com/xap/1.0/",
        "xmpMM": "http://ns.adobe.com/xap/1.0/mm/",
        "stEvt": "http://ns.adobe.com/xap/1.0/sType/ResourceEvent#",
        "tiff": "http://ns.adobe.com/tiff/1.0/",
        "exif": "http://ns.adobe.com/exif/1.0/",
        "aux": "http://ns.adobe.com/exif/1.0/aux/",
        "exifEX": "http://cipa.jp/exif/1.0/",
        "photoshop": "http://ns.adobe.com/photoshop/1.0/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "crd": "http://ns.adobe.com/camera-raw-defaults/1.0/",
        "xmpDM": "http://ns.adobe.com/xmp/1.0/DynamicMedia/",
        "crs": "http://ns.adobe.com/camera-raw-settings/1.0/",
    }

    @staticmethod
    def parse_datetime(date_str: str | None) -> datetime | None:
        """ISO 8601形式の日時文字列をdatetimeオブジェクトに変換。

        Args:
            date_str: ISO 8601形式の日時文字列

        Returns:
            datetimeオブジェクト、またはNone
        """
        if not date_str:
            return None

        try:
            # タイムゾーン付きのISO 8601形式をパース
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def parse_fraction(fraction_str: str | None) -> float | None:
        """分数形式の文字列を浮動小数点数に変換。

        Args:
            fraction_str: 分数形式の文字列（例: "1/100", "28/10"）

        Returns:
            浮動小数点数、またはNone
        """
        if not fraction_str:
            return None

        try:
            if "/" in fraction_str:
                numerator, denominator = fraction_str.split("/")
                return float(numerator) / float(denominator)
            return float(fraction_str)
        except (ValueError, ZeroDivisionError):
            return None

    def parse(self, file_path: str | Path) -> XMPMetadata:
        """XMPファイルをパースしてXMPMetadataオブジェクトを生成。

        Args:
            file_path: XMPファイルのパス

        Returns:
            XMPMetadataオブジェクト

        Raises:
            FileNotFoundError: ファイルが存在しない場合
            ET.ParseError: XMLのパースに失敗した場合
        """
        file_path = Path(file_path)
        if not file_path.exists():
            logger.error(f"XMP file not found: {file_path}")
            raise FileNotFoundError(f"XMP file not found: {file_path}")

        tree = ET.parse(file_path)
        root = tree.getroot()

        description = root.find(".//rdf:Description", self.NAMESPACES)
        if description is None:
            logger.warning(f"XMP file is empty: {file_path}")
            return XMPMetadata()

        metadata = XMPMetadata()
        metadata.xmp_info = XmpBasicInfo(
            creator_tool=description.get(f"{{{self.NAMESPACES['xmp']}}}CreatorTool"),
            modify_date=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['xmp']}}}ModifyDate")
            ),
            create_date=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['xmp']}}}CreateDate")
            ),
            metadata_date=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['xmp']}}}MetadataDate")
            ),
            # Rating要素を追加（1-5の範囲、または None）
            rating=int(description.get(f"{{{self.NAMESPACES['xmp']}}}Rating", "0"))
            if description.get(f"{{{self.NAMESPACES['xmp']}}}Rating")
            else None,
            # Label要素を追加
            label=description.get(f"{{{self.NAMESPACES['xmp']}}}Label"),
        )

        metadata.document_info = XmpDocumentInfo(
            document_id=description.get(f"{{{self.NAMESPACES['xmpMM']}}}DocumentID"),
            instance_id=description.get(f"{{{self.NAMESPACES['xmpMM']}}}InstanceID"),
            preserved_file_name=description.get(
                f"{{{self.NAMESPACES['xmpMM']}}}PreservedFileName"
            ),
            original_document_id=description.get(
                f"{{{self.NAMESPACES['xmpMM']}}}OriginalDocumentID"
            ),
        )

        metadata.tiff_info = TiffInfo(
            make=description.get(f"{{{self.NAMESPACES['tiff']}}}Make"),
            model=description.get(f"{{{self.NAMESPACES['tiff']}}}Model"),
            orientation=int(
                description.get(f"{{{self.NAMESPACES['tiff']}}}Orientation", "1")
            ),
            image_width=int(
                description.get(f"{{{self.NAMESPACES['tiff']}}}ImageWidth", "0")
            ),
            image_length=int(
                description.get(f"{{{self.NAMESPACES['tiff']}}}ImageLength", "0")
            ),
            # 解像度情報を追加
            x_resolution=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['tiff']}}}XResolution")
            ),
            y_resolution=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['tiff']}}}YResolution")
            ),
            resolution_unit=int(
                description.get(f"{{{self.NAMESPACES['tiff']}}}ResolutionUnit", "0")
            )
            if description.get(f"{{{self.NAMESPACES['tiff']}}}ResolutionUnit")
            else None,
        )

        metadata.exif_info = ExifInfo(
            exposure_time=description.get(f"{{{self.NAMESPACES['exif']}}}ExposureTime"),
            shutter_speed_value=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}ShutterSpeedValue")
            ),
            f_number=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}FNumber")
            ),
            aperture_value=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}ApertureValue")
            ),
            exposure_program=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}ExposureProgram", "0")
            ),
            exposure_mode=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}ExposureMode", "0")
            ),
            exposure_bias_value=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}ExposureBiasValue")
            ),
            recommended_exposure_index=int(
                description.get(
                    f"{{{self.NAMESPACES['exif']}}}RecommendedExposureIndex", "0"
                )
            ),
            sensitivity_type=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}SensitivityType", "0")
            ),
            metering_mode=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}MeteringMode", "0")
            ),
            light_source=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}LightSource", "0")
            ),
            white_balance=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}WhiteBalance", "0")
            ),
            brightness_value=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}BrightnessValue")
            ),
            focal_length=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}FocalLength")
            ),
            focal_length_in_35mm_film=int(
                description.get(
                    f"{{{self.NAMESPACES['exif']}}}FocalLengthIn35mmFilm", "0"
                )
            ),
            max_aperture_value=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}MaxApertureValue")
            ),
            digital_zoom_ratio=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}DigitalZoomRatio")
            ),
            pixel_x_dimension=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}PixelXDimension", "0")
            ),
            pixel_y_dimension=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}PixelYDimension", "0")
            ),
            focal_plane_x_resolution=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}FocalPlaneXResolution")
            ),
            focal_plane_y_resolution=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['exif']}}}FocalPlaneYResolution")
            ),
            focal_plane_resolution_unit=int(
                description.get(
                    f"{{{self.NAMESPACES['exif']}}}FocalPlaneResolutionUnit", "0"
                )
            ),
            custom_rendered=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}CustomRendered", "0")
            ),
            scene_capture_type=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}SceneCaptureType", "0")
            ),
            contrast=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}Contrast", "0")
            ),
            saturation=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}Saturation", "0")
            ),
            sharpness=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}Sharpness", "0")
            ),
            file_source=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}FileSource", "0")
            ),
            scene_type=int(
                description.get(f"{{{self.NAMESPACES['exif']}}}SceneType", "0")
            ),
            exif_version=description.get(f"{{{self.NAMESPACES['exif']}}}ExifVersion"),
            date_time_original=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['exif']}}}DateTimeOriginal")
            ),
            # ExifInfoの追加フィールド
            date_time_digitized=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['exif']}}}DateTimeDigitized")
            ),
        )

        iso_elem = description.find(
            ".//exif:ISOSpeedRatings/rdf:Seq/rdf:li", self.NAMESPACES
        )
        if iso_elem is not None and iso_elem.text:
            metadata.exif_info.iso_speed_ratings = [int(iso_elem.text)]

        flash_elem = description.find(".//exif:Flash", self.NAMESPACES)
        if flash_elem is not None:
            metadata.flash_info = FlashInfo(
                fired=flash_elem.get(
                    f"{{{self.NAMESPACES['exif']}}}Fired", "False"
                ).lower()
                == "true",
                return_mode=int(
                    flash_elem.get(f"{{{self.NAMESPACES['exif']}}}Return", "0")
                ),
                mode=int(flash_elem.get(f"{{{self.NAMESPACES['exif']}}}Mode", "0")),
                function=flash_elem.get(
                    f"{{{self.NAMESPACES['exif']}}}Function", "False"
                ).lower()
                == "true",
                red_eye_mode=flash_elem.get(
                    f"{{{self.NAMESPACES['exif']}}}RedEyeMode", "False"
                ).lower()
                == "true",
            )

        metadata.lens_info = LensInfo(
            lens_info=description.get(f"{{{self.NAMESPACES['aux']}}}LensInfo"),
            lens=description.get(f"{{{self.NAMESPACES['aux']}}}Lens"),
            lens_model=description.get(f"{{{self.NAMESPACES['exifEX']}}}LensModel"),
            lens_distort_info=description.get(
                f"{{{self.NAMESPACES['aux']}}}LensDistortInfo"
            ),
            # LensInfoの追加フィールド
            lens_serial_number=description.get(
                f"{{{self.NAMESPACES['aux']}}}LensSerialNumber"
            ),
        )

        metadata.photoshop_info = PhotoshopInfo(
            date_created=self.parse_datetime(
                description.get(f"{{{self.NAMESPACES['photoshop']}}}DateCreated")
            ),
            sidecar_for_extension=description.get(
                f"{{{self.NAMESPACES['photoshop']}}}SidecarForExtension"
            ),
            embedded_xmp_digest=description.get(
                f"{{{self.NAMESPACES['photoshop']}}}EmbeddedXMPDigest"
            ),
            # 追加フィールド
            color_mode=int(
                description.get(f"{{{self.NAMESPACES['photoshop']}}}ColorMode", "0")
            )
            if description.get(f"{{{self.NAMESPACES['photoshop']}}}ColorMode")
            else None,
            icc_profile=description.get(
                f"{{{self.NAMESPACES['photoshop']}}}ICCProfile"
            ),
        )

        metadata.camera_raw_settings = CameraRawSettings(
            crop_top=float(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropTop", "0")
            ),
            crop_left=float(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropLeft", "0")
            ),
            crop_bottom=float(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropBottom", "1")
            ),
            crop_right=float(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropRight", "1")
            ),
            crop_angle=float(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropAngle", "0")
            ),
            crop_constrain_to_warp=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}CropConstrainToWarp", "0")
            ),
            crop_constrain_to_unit_square=int(
                description.get(
                    f"{{{self.NAMESPACES['crs']}}}CropConstrainToUnitSquare", "1"
                )
            ),
            has_crop=description.get(
                f"{{{self.NAMESPACES['crs']}}}HasCrop", "False"
            ).lower()
            == "true",
            already_applied=description.get(
                f"{{{self.NAMESPACES['crs']}}}AlreadyApplied", "False"
            ).lower()
            == "true",
            raw_file_name=description.get(f"{{{self.NAMESPACES['crs']}}}RawFileName"),
            camera_profile=description.get(
                f"{{{self.NAMESPACES['crd']}}}CameraProfile"
            ),
            look_name=description.get(f"{{{self.NAMESPACES['crd']}}}LookName"),
            # Camera Rawバージョン情報を追加
            version=description.get(f"{{{self.NAMESPACES['crs']}}}Version"),
            process_version=description.get(
                f"{{{self.NAMESPACES['crs']}}}ProcessVersion"
            ),
            # 調整パラメータを追加
            exposure=self.parse_fraction(
                description.get(f"{{{self.NAMESPACES['crs']}}}Exposure2012")
            ),
            contrast=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}Contrast2012", "0")
            )
            if description.get(f"{{{self.NAMESPACES['crs']}}}Contrast2012")
            else None,
            highlights=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}Highlights2012", "0")
            )
            if description.get(f"{{{self.NAMESPACES['crs']}}}Highlights2012")
            else None,
            shadows=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}Shadows2012", "0")
            )
            if description.get(f"{{{self.NAMESPACES['crs']}}}Shadows2012")
            else None,
            whites=int(description.get(f"{{{self.NAMESPACES['crs']}}}Whites2012", "0"))
            if description.get(f"{{{self.NAMESPACES['crs']}}}Whites2012")
            else None,
            blacks=int(description.get(f"{{{self.NAMESPACES['crs']}}}Blacks2012", "0"))
            if description.get(f"{{{self.NAMESPACES['crs']}}}Blacks2012")
            else None,
            clarity=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}Clarity2012", "0")
            )
            if description.get(f"{{{self.NAMESPACES['crs']}}}Clarity2012")
            else None,
            vibrance=int(description.get(f"{{{self.NAMESPACES['crs']}}}Vibrance", "0"))
            if description.get(f"{{{self.NAMESPACES['crs']}}}Vibrance")
            else None,
            saturation=int(
                description.get(f"{{{self.NAMESPACES['crs']}}}Saturation", "0")
            )
            if description.get(f"{{{self.NAMESPACES['crs']}}}Saturation")
            else None,
        )

        # Dublin Core情報の拡張
        metadata.dublin_core_info = DublinCoreInfo(
            format=description.get(f"{{{self.NAMESPACES['dc']}}}format"),
            title=description.get(f"{{{self.NAMESPACES['dc']}}}title"),
            description=description.get(f"{{{self.NAMESPACES['dc']}}}description"),
            rights=description.get(f"{{{self.NAMESPACES['dc']}}}rights"),
        )

        # Dublin Core のリスト要素の処理
        creator_elem = description.find(".//dc:creator/rdf:Bag/rdf:li", self.NAMESPACES)
        if creator_elem is not None and creator_elem.text:
            metadata.dublin_core_info.creator = [creator_elem.text]

        subject_elems = description.findall(
            ".//dc:subject/rdf:Bag/rdf:li", self.NAMESPACES
        )
        if subject_elems:
            metadata.dublin_core_info.subject = [
                elem.text for elem in subject_elems if elem.text
            ]

        metadata.dynamic_media_info = DynamicMediaInfo(
            pick=int(description.get(f"{{{self.NAMESPACES['xmpDM']}}}pick", "0")),
            # 追加フィールド
            good=description.get(f"{{{self.NAMESPACES['xmpDM']}}}good", "False").lower()
            == "true"
            if description.get(f"{{{self.NAMESPACES['xmpDM']}}}good")
            else None,
            scene=description.get(f"{{{self.NAMESPACES['xmpDM']}}}scene"),
        )

        return metadata


if __name__ == "__main__":
    configure_loguru(verbose=True)

    rating_xmp_file = Path("tests/assets/rating_1.xmp")
    not_rating_xmp_file = Path("tests/assets/not_rating.xmp")

    # クラスベースの使用例
    parser = XMPParser()

    logger.info(f"Parsing XMP file: {rating_xmp_file}")
    metadata = parser.parse(rating_xmp_file)
    logger.info(f"RawImageName: {metadata.camera_raw_settings.raw_file_name}")
    logger.info(f"Rating: {metadata.xmp_info.rating}")

    logger.info(f"Parsing XMP file: {not_rating_xmp_file}")
    metadata = parser.parse(not_rating_xmp_file)
    logger.info(f"RawImageName: {metadata.camera_raw_settings.raw_file_name}")
    logger.info(f"Rating: {metadata.xmp_info.rating}")
