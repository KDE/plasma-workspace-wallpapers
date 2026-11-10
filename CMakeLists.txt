cmake_minimum_required(VERSION 3.16)

project(wallpapers)
set(PROJECT_VERSION "6.8.80")

include(WriteBasicConfigVersionFile)
include(FeatureSummary)

set(KF6_MIN_VERSION "6.30.0")
set(KDE_COMPILERSETTINGS_LEVEL "6.0")

find_package(ECM ${KF6_MIN_VERSION} REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH} )

include(KDEInstallDirs)
include(KDECMakeSettings)
include(KDECompilerSettings)
include(GenerateExportHeader)

set(_wallpaper_directories
    Autumn
    BytheWater
    Canopee
    Cascade
    Cluster
    ColdRipple
    ColorfulCups
    DarkestHour
    Elarun
    EveningGlow
    FallenLeaf
    FlyingKonqui
    Grey
    IceCold
    Kite
    Kokkini
    OneStandsOut
    Opal
    PastelHills
    Path
    SafeLanding
    Shell
    summer_1am
    Volna
    Flow
    MilkyWay
    Altai
    Patak
    Honeywave
    Kay
    Mountain
    ScarletTree
    Nexus
    Nuvole
    Coast
    Orionids
    Sub-Arctic
    Waterfall
)

foreach(_wallpaper IN LISTS _wallpaper_directories)
    file(GLOB_RECURSE _wallpaper_webp_images
        LIST_DIRECTORIES false
        "${CMAKE_CURRENT_SOURCE_DIR}/${_wallpaper}/*.webp"
    )
    if(NOT _wallpaper_webp_images)
        message(FATAL_ERROR "No WebP images found in ${_wallpaper}; run tools/convert-images.py")
    endif()

    install(DIRECTORY "${_wallpaper}"
        DESTINATION ${KDE_INSTALL_WALLPAPERDIR}
        PATTERN "*.png" EXCLUDE
        PATTERN "*.jpg" EXCLUDE
        PATTERN "*.jpeg" EXCLUDE
    )
endforeach()
