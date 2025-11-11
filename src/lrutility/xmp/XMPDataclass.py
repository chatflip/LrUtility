from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class XmpBasicInfo:
    """XMP基本情報を格納するデータクラス。"""

    creator_tool: str | None = None  # カメラのファームウェア情報
    modify_date: datetime | None = None  # 最終更新日時
    create_date: datetime | None = None  # 作成日時
    metadata_date: datetime | None = None  # メタデータ更新日時
    rating: int | None = None  # レーティング（1-5）
    label: str | None = None  # ラベル


@dataclass
class XmpDocumentInfo:
    """XMPドキュメント管理情報を格納するデータクラス。"""

    document_id: str | None = None  # ドキュメントID (UUID)
    instance_id: str | None = None  # インスタンスID
    preserved_file_name: str | None = None  # 元のファイル名
    original_document_id: str | None = None  # オリジナルドキュメントID
    history: list[dict[str, str]] = field(
        default_factory=list
    )  # 編集履歴 # type: ignore[assignment]


@dataclass
class TiffInfo:
    """TIFF関連情報を格納するデータクラス。"""

    make: str | None = None  # カメラメーカー（例: SONY）
    model: str | None = None  # カメラモデル（例: ILCE-7M4）
    orientation: int | None = None  # 画像の向き（1-8）
    image_width: int | None = None  # 画像幅（ピクセル）
    image_length: int | None = None  # 画像高さ（ピクセル）
    x_resolution: float | None = None  # X解像度
    y_resolution: float | None = None  # Y解像度
    resolution_unit: int | None = None  # 解像度単位


@dataclass
class ExifInfo:
    """EXIF撮影情報を格納するデータクラス。"""

    # 露出設定
    exposure_time: str | None = None  # シャッタースピード（例: "1/100"）
    shutter_speed_value: float | None = None  # シャッタースピード値
    f_number: float | None = None  # F値
    aperture_value: float | None = None  # 絞り値
    exposure_program: int | None = None  # 露出プログラム（1=マニュアル等）
    exposure_mode: int | None = None  # 露出モード
    exposure_bias_value: float | None = None  # 露出補正値

    # ISO感度
    iso_speed_ratings: list[int] | None = None  # ISO感度
    sensitivity_type: int | None = None  # 感度タイプ
    recommended_exposure_index: int | None = None  # 推奨露出指数

    # 測光・ホワイトバランス
    metering_mode: int | None = None  # 測光モード（5=パターン等）
    light_source: int | None = None  # 光源
    white_balance: int | None = None  # ホワイトバランス（0=自動）
    brightness_value: float | None = None  # 明るさ値

    # レンズ・焦点距離
    focal_length: float | None = None  # 焦点距離（mm）
    focal_length_in_35mm_film: int | None = None  # 35mm換算焦点距離
    max_aperture_value: float | None = None  # 最大絞り値
    digital_zoom_ratio: float | None = None  # デジタルズーム比率

    # 画像情報
    pixel_x_dimension: int | None = None  # 有効画素幅
    pixel_y_dimension: int | None = None  # 有効画素高
    focal_plane_x_resolution: float | None = None  # 焦点面X解像度
    focal_plane_y_resolution: float | None = None  # 焦点面Y解像度
    focal_plane_resolution_unit: int | None = None  # 焦点面解像度単位

    # その他の設定
    custom_rendered: int | None = None  # カスタムレンダリング
    scene_capture_type: int | None = None  # シーンキャプチャタイプ
    contrast: int | None = None  # コントラスト
    saturation: int | None = None  # 彩度
    sharpness: int | None = None  # シャープネス

    # ファイル情報
    file_source: int | None = None  # ファイルソース（3=DSC）
    scene_type: int | None = None  # シーンタイプ
    exif_version: str | None = None  # EXIFバージョン

    # 日時情報
    date_time_original: datetime | None = None  # 撮影日時
    date_time_digitized: datetime | None = None  # デジタル化日時


@dataclass
class FlashInfo:
    """フラッシュ情報を格納するデータクラス。"""

    fired: bool = False  # フラッシュ発光有無
    return_mode: int | None = None  # リターンモード
    mode: int | None = None  # フラッシュモード（2=強制OFF等）
    function: bool = False  # フラッシュ機能
    red_eye_mode: bool = False  # 赤目軽減モード


@dataclass
class LensInfo:
    """レンズ情報を格納するデータクラス。"""

    lens_info: str | None = None  # レンズ情報（焦点距離範囲、F値範囲）
    lens: str | None = None  # レンズ名（例: "FE 70-200mm F2.8 GM OSS II"）
    lens_model: str | None = None  # レンズモデル名
    lens_distort_info: str | None = None  # レンズ歪み補正情報
    lens_serial_number: str | None = None  # レンズシリアル番号


@dataclass
class PhotoshopInfo:
    """Photoshop/Adobe関連情報を格納するデータクラス。"""

    date_created: datetime | None = None  # 作成日時
    sidecar_for_extension: str | None = None  # サイドカーファイルの拡張子（例: "ARW"）
    embedded_xmp_digest: str | None = None  # 埋め込みXMPダイジェスト
    color_mode: int | None = None  # カラーモード
    icc_profile: str | None = None  # ICCプロファイル


@dataclass
class CameraRawSettings:
    """Camera Raw（Lightroom）設定を格納するデータクラス。"""

    # クロップ設定
    crop_top: float = 0.0  # クロップ上端（0-1）
    crop_left: float = 0.0  # クロップ左端（0-1）
    crop_bottom: float = 1.0  # クロップ下端（0-1）
    crop_right: float = 1.0  # クロップ右端（0-1）
    crop_angle: float = 0.0  # クロップ角度
    crop_constrain_to_warp: int = 0  # ワープに制約
    crop_constrain_to_unit_square: int = 1  # 正方形に制約
    has_crop: bool = False  # クロップ有無

    # 基本設定
    already_applied: bool = False  # 設定適用済み
    raw_file_name: str | None = None  # RAWファイル名
    version: str | None = None  # Camera Rawバージョン
    process_version: str | None = None  # プロセスバージョン

    # カメラプロファイル
    camera_profile: str | None = None  # カメラプロファイル（例: "Camera ST"）
    look_name: str | None = None  # ルック名

    # 調整パラメータ（今後拡張可能）
    exposure: float | None = None  # 露出補正
    contrast: int | None = None  # コントラスト
    highlights: int | None = None  # ハイライト
    shadows: int | None = None  # シャドウ
    whites: int | None = None  # 白レベル
    blacks: int | None = None  # 黒レベル
    clarity: int | None = None  # 明瞭度
    vibrance: int | None = None  # 自然な彩度
    saturation: int | None = None  # 彩度


@dataclass
class DublinCoreInfo:
    """Dublin Coreメタデータを格納するデータクラス。"""

    format: str | None = None  # ファイル形式（例: "image/x-sony-arw"）
    title: str | None = None  # タイトル
    creator: list[str] | None = None  # 作成者
    subject: list[str] | None = None  # キーワード
    description: str | None = None  # 説明
    rights: str | None = None  # 著作権


@dataclass
class DynamicMediaInfo:
    """Dynamic Media（xmpDM）情報を格納するデータクラス。"""

    pick: int = 0  # ピックフラグ（0=なし、1=採用、-1=除外）
    good: bool | None = None  # 良好フラグ
    scene: str | None = None  # シーン名


@dataclass
class XMPMetadata:
    """XMPメタデータ全体を格納する統合データクラス。

    このクラスは、カメラのXMPファイルから抽出される
    すべてのメタデータを統合的に管理します。

    Attributes:
        xmp_info: XMP基本情報
        document_info: ドキュメント管理情報
        tiff_info: TIFF関連情報
        exif_info: EXIF撮影情報
        flash_info: フラッシュ情報
        lens_info: レンズ情報
        photoshop_info: Photoshop/Adobe関連情報
        camera_raw_settings: Camera Raw（Lightroom）設定
        dublin_core_info: Dublin Coreメタデータ
        dynamic_media_info: Dynamic Media情報
    """

    xmp_info: XmpBasicInfo = field(default_factory=XmpBasicInfo)
    document_info: XmpDocumentInfo = field(default_factory=XmpDocumentInfo)
    tiff_info: TiffInfo = field(default_factory=TiffInfo)
    exif_info: ExifInfo = field(default_factory=ExifInfo)
    flash_info: FlashInfo = field(default_factory=FlashInfo)
    lens_info: LensInfo = field(default_factory=LensInfo)
    photoshop_info: PhotoshopInfo = field(default_factory=PhotoshopInfo)
    camera_raw_settings: CameraRawSettings = field(default_factory=CameraRawSettings)
    dublin_core_info: DublinCoreInfo = field(default_factory=DublinCoreInfo)
    dynamic_media_info: DynamicMediaInfo = field(default_factory=DynamicMediaInfo)

    def __repr__(self) -> str:
        return f"""
        XMPMetadata(
            xmp_info={self.xmp_info},
            document_info={self.document_info},
            tiff_info={self.tiff_info},
            exif_info={self.exif_info},
            flash_info={self.flash_info},
            lens_info={self.lens_info},
            photoshop_info={self.photoshop_info},
            camera_raw_settings={self.camera_raw_settings},
            dublin_core_info={self.dublin_core_info},
            dynamic_media_info={self.dynamic_media_info},
        )
        """
