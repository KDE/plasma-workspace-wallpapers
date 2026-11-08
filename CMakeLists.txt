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

set(WALLPAPER_IMAGE_FORMAT "" CACHE STRING "Convert wallpaper images to JPEG or WebP (empty keeps the original formats)")
set_property(CACHE WALLPAPER_IMAGE_FORMAT PROPERTY STRINGS "" JPEG WEBP)
string(TOUPPER "${WALLPAPER_IMAGE_FORMAT}" _wallpaper_image_format)

if(_wallpaper_image_format AND NOT _wallpaper_image_format MATCHES "^(JPEG|WEBP)$")
    message(FATAL_ERROR "WALLPAPER_IMAGE_FORMAT must be JPEG or WEBP")
endif()

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

if(_wallpaper_image_format)
    find_program(_image_magick_executable NAMES magick)
    if(NOT _image_magick_executable)
        find_program(_image_magick_executable NAMES convert)
    endif()
    if(NOT _image_magick_executable)
        message(FATAL_ERROR "ImageMagick is required when WALLPAPER_IMAGE_FORMAT is set")
    endif()

    if(_wallpaper_image_format STREQUAL "JPEG")
        set(_wallpaper_image_extension ".jpg")
    else()
        set(_wallpaper_image_extension ".webp")
    endif()

    set(_wallpaper_image_sources)
    foreach(_wallpaper IN LISTS _wallpaper_directories)
        file(GLOB_RECURSE _wallpaper_images
            CONFIGURE_DEPENDS
            LIST_DIRECTORIES false
            RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
            "${CMAKE_CURRENT_SOURCE_DIR}/${_wallpaper}/*.png"
            "${CMAKE_CURRENT_SOURCE_DIR}/${_wallpaper}/*.jpg"
            "${CMAKE_CURRENT_SOURCE_DIR}/${_wallpaper}/*.jpeg"
            "${CMAKE_CURRENT_SOURCE_DIR}/${_wallpaper}/*.webp"
        )
        list(APPEND _wallpaper_image_sources ${_wallpaper_images})
    endforeach()

    set(_converted_wallpaper_images)
    set(_converted_wallpaper_image_outputs)
    foreach(_image IN LISTS _wallpaper_image_sources)
        get_filename_component(_image_directory "${_image}" DIRECTORY)
        get_filename_component(_image_name "${_image}" NAME_WE)
        set(_output "${CMAKE_CURRENT_BINARY_DIR}/converted/${_image_directory}/${_image_name}${_wallpaper_image_extension}")
        list(FIND _converted_wallpaper_image_outputs "${_output}" _output_index)
        if(NOT _output_index EQUAL -1)
            message(FATAL_ERROR "Multiple source images map to ${_output}")
        endif()
        list(APPEND _converted_wallpaper_image_outputs "${_output}")
        get_filename_component(_output_directory "${_output}" DIRECTORY)
        add_custom_command(
            OUTPUT "${_output}"
            COMMAND "${CMAKE_COMMAND}" -E make_directory "${_output_directory}"
            COMMAND "${_image_magick_executable}" "${CMAKE_CURRENT_SOURCE_DIR}/${_image}" "${_output}"
            DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/${_image}"
            VERBATIM
        )
        file(RELATIVE_PATH _output_relative_path "${CMAKE_CURRENT_BINARY_DIR}/converted" "${_output}")
        get_filename_component(_output_relative_directory "${_output_relative_path}" DIRECTORY)
        install(FILES "${_output}" DESTINATION "${KDE_INSTALL_WALLPAPERDIR}/${_output_relative_directory}")
        list(APPEND _converted_wallpaper_images "${_output}")
    endforeach()

    add_custom_target(convert_wallpaper_images ALL DEPENDS ${_converted_wallpaper_images})
endif()

foreach(_wallpaper IN LISTS _wallpaper_directories)
    if(_wallpaper_image_format)
        install(DIRECTORY "${_wallpaper}"
            DESTINATION ${KDE_INSTALL_WALLPAPERDIR}
            PATTERN "*.png" EXCLUDE
            PATTERN "*.jpg" EXCLUDE
            PATTERN "*.jpeg" EXCLUDE
            PATTERN "*.webp" EXCLUDE
        )
    else()
        install(DIRECTORY "${_wallpaper}" DESTINATION ${KDE_INSTALL_WALLPAPERDIR})
    endif()
endforeach()
