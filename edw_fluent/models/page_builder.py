# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings


DEFAULT_ELEMENTS = {
    'DataMartItem': {
        "Data marts": [
            {
                "url": "elements/datamarts/tpl/default_with_tree.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_with_tree.jpg"
            },
            {
                "url": "elements/datamarts/tpl/default_related.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_related.jpg"
            },
            {
                "url": "elements/datamarts/tpl/default_related_with_title.html",
                "height": 347,
                "thumbnail": "elements/datamarts/thumbs/default_related_with_title.jpg"
            }
        ]
    },
    'TemplateItem': {
        "Text Grid": [
            {
                "url": "elements/text/tpl/text-1col.html",
                "height": 637,
                "thumbnail": "elements/text/thumbs/text-1col.jpg"
            },
            {
                "url": "elements/text/tpl/text-2col.html",
                "height": 547,
                "thumbnail": "elements/text/thumbs/text-2col.jpg"
            },
            {
                "url": "elements/text/tpl/text-3col.html",
                "height": 547,
                "thumbnail": "elements/text/thumbs/text-3col.jpg"
            },
            {
                "url": "elements/text/tpl/text-4col.html",
                "height": 540,
                "thumbnail": "elements/text/thumbs/text-4col.jpg"
            },
        ],
        "Team": [
            {
                "url": "elements/team/tpl/team-circle.html",
                "height": 929,
                "thumbnail": "elements/team/thumbs/team-circle.jpg"
            },
            {
                "url": "elements/team/tpl/team-circle-2.html",
                "height": 929,
                "thumbnail": "elements/team/thumbs/team-circle-2.jpg"
            },
            {
                "url": "elements/team/tpl/team.html",
                "height": 989,
                "thumbnail": "elements/team/thumbs/team.jpg"
            },
            {
                "url": "elements/team/tpl/team-4col.html",
                "height": 940,
                "thumbnail": "elements/team/thumbs/team-4col.jpg"
            },
            {
                "url": "elements/team/tpl/team-full.html",
                "height": 959,
                "thumbnail": "elements/team/thumbs/team-full.jpg"
            },
            {
                "url": "elements/team/tpl/team-border.html",
                "height": 1258,
                "thumbnail": "elements/team/thumbs/team-border.jpg"
            }
        ],
        "Video": [
            {
                "url": "elements/video/tpl/video-full.html",
                "height": 1160,
                "thumbnail": "elements/video/thumbs/video-full.jpg"
            },
            {
                "url": "elements/video/tpl/video-half-left-2.html",
                "height": 612,
                "thumbnail": "elements/video/thumbs/video-half-left-2.jpg"
            },
            {
                "url": "elements/video/tpl/video-half-right.html",
                "height": 640,
                "thumbnail": "elements/video/thumbs/video-half-right.jpg"
            },
            {
                "url": "elements/video/tpl/video-half-left.html",
                "height": 640,
                "thumbnail": "elements/video/thumbs/video-half-left.jpg"
            },
            {
                "url": "elements/video/tpl/video-half-left-3.html",
                "height": 634,
                "thumbnail": "elements/video/thumbs/video-half-left-3.jpg"
            },
            {
                "url": "elements/video/tpl/video-popup.html",
                "height": 577,
                "thumbnail": "elements/video/thumbs/video-popup.jpg"
            }
        ],
        "Contact": [
            {
                "url": "elements/contact/tpl/map-full.html",
                "height": 1308,
                "thumbnail": "elements/contact/thumbs/map-full.jpg"
            },
            {
                "url": "elements/contact/tpl/map-half.html",
                "height": 717,
                "thumbnail": "elements/contact/thumbs/map-half.jpg"
            },
            {
                "url": "elements/contact/tpl/map-half-left.html",
                "height": 717,
                "thumbnail": "elements/contact/thumbs/map-half-left.jpg"
            },
            {
                "url": "elements/contact/tpl/map-half-left-2.html",
                "height": 722,
                "thumbnail": "elements/contact/thumbs/map-half-left-2.jpg"
            },
            {
                "url": "elements/contact/tpl/map-full-2.html",
                "height": 601,
                "thumbnail": "elements/contact/thumbs/map-full-2.jpg"
            },
            {
                "url": "elements/contact/tpl/map-full-3.html",
                "height": 1230,
                "thumbnail": "elements/contact/thumbs/map-full-3.jpg"
            },
            {
                "url": "elements/contact/tpl/map-full-4.html",
                "height": 720,
                "thumbnail": "elements/contact/thumbs/map-full-4.jpg"
            },
        ],
        "Pricing Tables": [
            {
                "url": "elements/pricing/tpl/pricing-4col.html",
                "height": 1154,
                "thumbnail": "elements/pricing/thumbs/pricing-4col.jpg"
            },
            {
                "url": "elements/pricing/tpl/pricing-3col.html",
                "height": 1154,
                "thumbnail": "elements/pricing/thumbs/pricing-3col.jpg"
            },
            {
                "url": "elements/pricing/tpl/pricing-4col-2.html",
                "height": 1011,
                "thumbnail": "elements/pricing/thumbs/pricing-4col-2.jpg"
            },
            {
                "url": "elements/pricing/tpl/pricing-3col-img.html",
                "height": 1184,
                "thumbnail": "elements/pricing/thumbs/pricing-3col-img.jpg"
            },
            {
                "url": "elements/pricing/tpl/pricing-2col-img.html",
                "height": 1159,
                "thumbnail": "elements/pricing/thumbs/pricing-2col-img.jpg"
            },
            {
                "url": "elements/pricing/tpl/pricing-2col-img-2.html",
                "height": 961,
                "thumbnail": "elements/pricing/thumbs/pricing-2col-img-2.jpg"
            }
        ],
        "Step-by-Step": [
            {
                "url": "elements/steps/tpl/steps-left.html",
                "height": 1759,
                "thumbnail": "elements/steps/thumbs/steps-left.jpg"
            },
            {
                "url": "elements/steps/tpl/steps-left-2.html",
                "height": 1758,
                "thumbnail": "elements/steps/thumbs/steps-left-2.jpg"
            },
            {
                "url": "elements/steps/tpl/steps-center.html",
                "height": 1919,
                "thumbnail": "elements/steps/thumbs/steps-center.jpg"
            },
            {
                "url": "elements/steps/tpl/steps-center-2.html",
                "height": 1918,
                "thumbnail": "elements/steps/thumbs/steps-center-2.jpg"
            },
            {
                "url": "elements/steps/tpl/steps-path.html",
                "height": 1919,
                "thumbnail": "elements/steps/thumbs/steps-path.jpg"
            },
            {
                "url": "elements/steps/tpl/steps-path-2.html",
                "height": 1918,
                "thumbnail": "elements/steps/thumbs/steps-path-2.jpg"
            },
        ],
        "Testimonials": [
            {
                "url": "elements/testimonials/tpl/testimonials-grid.html",
                "height": 1030,
                "thumbnail": "elements/testimonials/thumbs/testimonials-grid.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-slider.html",
                "height": 579,
                "thumbnail": "elements/testimonials/thumbs/testimonials-slider.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-slider-2.html",
                "height": 579,
                "thumbnail": "elements/testimonials/thumbs/testimonials-slider-2.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-slider-3.html",
                "height": 449,
                "thumbnail": "elements/testimonials/thumbs/testimonials-slider-3.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients.html",
                "height": 310,
                "thumbnail": "elements/testimonials/thumbs/clients.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients-slider-2.html",
                "height": 361,
                "thumbnail": "elements/testimonials/thumbs/clients-slider-2.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-grid-left.html",
                "height": 1032,
                "thumbnail": "elements/testimonials/thumbs/testimonials-grid-left.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-grid-2.html",
                "height": 1030,
                "thumbnail": "elements/testimonials/thumbs/testimonials-grid-2.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients-slider.html",
                "height": 361,
                "thumbnail": "elements/testimonials/thumbs/clients-slider.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-slider-star.html",
                "height": 557,
                "thumbnail": "elements/testimonials/thumbs/testimonials-slider-star.jpg"
            },
            {
                "url": "elements/testimonials/tpl/testimonials-slider-star-2.html",
                "height": 551,
                "thumbnail": "elements/testimonials/thumbs/testimonials-slider-star-2.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients-grid-link.html",
                "height": 654,
                "thumbnail": "elements/testimonials/thumbs/clients-grid-link.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients-grid.html",
                "height": 872,
                "thumbnail": "elements/testimonials/thumbs/clients-grid.jpg"
            },
            {
                "url": "elements/testimonials/tpl/clients-2.html",
                "height": 171,
                "thumbnail": "elements/testimonials/thumbs/clients-2.jpg"
            },
        ],
        "Content": [
            {
                "url": "elements/content/tpl/complex-title.html",
                "height": 740,
                "thumbnail": "elements/content/thumbs/complex-title.jpg"
            },
            {
                "url": "elements/content/tpl/content-right.html",
                "height": 740,
                "thumbnail": "elements/content/thumbs/content-right.jpg"
            },
            {
                "url": "elements/content/tpl/content-half-right.html",
                "height": 577,
                "thumbnail": "elements/content/thumbs/content-half-right.jpg"
            },
            {
                "url": "elements/content/tpl/content-half-right-2.html",
                "height": 577,
                "thumbnail": "elements/content/thumbs/content-half-right-2.jpg"
            },
            {
                "url": "elements/content/tpl/content-half-left.html",
                "height": 577,
                "thumbnail": "elements/content/thumbs/content-half-left.jpg"
            },
            {
                "url": "elements/content/tpl/content-full-right.html",
                "height": 645,
                "thumbnail": "elements/content/thumbs/content-full-right.jpg"
            },
            {
                "url": "elements/content/tpl/content-full-left.html",
                "height": 645,
                "thumbnail": "elements/content/thumbs/content-full-left.jpg"
            },
            {
                "url": "elements/content/tpl/content-full-right-2.html",
                "height": 699,
                "thumbnail": "elements/content/thumbs/content-full-right-2.jpg"
            },
            {
                "url": "elements/content/tpl/content-line.html",
                "height": 536,
                "thumbnail": "elements/content/thumbs/content-line.jpg"
            },
            {
                "url": "elements/content/tpl/content-line-2.html",
                "height": 437,
                "thumbnail": "elements/content/thumbs/content-line-2.jpg"
            },
            {
                "url": "elements/content/tpl/content-center-2.html",
                "height": 660,
                "thumbnail": "elements/content/thumbs/content-center-2.jpg"
            },
            {
                "url": "elements/content/tpl/content-center.html",
                "height": 745,
                "thumbnail": "elements/content/thumbs/content-center.jpg"
            },
            {
                "url": "elements/content/tpl/content-right-app.html",
                "height": 836,
                "thumbnail": "elements/content/thumbs/content-right-app.jpg"
            },
            {
                "url": "elements/content/tpl/content-left-app.html",
                "height": 746,
                "thumbnail": "elements/content/thumbs/content-left-app.jpg"
            },
            {
                "url": "elements/content/tpl/content-4col-full.html",
                "height": 400,
                "thumbnail": "elements/content/thumbs/content-4col-full.jpg"
            },
            {
                "url": "elements/content/tpl/content-left.html",
                "height": 671,
                "thumbnail": "elements/content/thumbs/content-left.jpg"
            },
            {
                "url": "elements/content/tpl/content-right-2.html",
                "height": 646,
                "thumbnail": "elements/content/thumbs/content-right-2.jpg"
            },
            {
                "url": "elements/content/tpl/items-3col.html",
                "height": 1587,
                "thumbnail": "elements/content/thumbs/items-3col.jpg"
            },
            {
                "url": "elements/content/tpl/items-3col-2.html",
                "height": 1177,
                "thumbnail": "elements/content/thumbs/items-3col-2.jpg"
            },
            {
                "url": "elements/content/tpl/items-3col-3.html",
                "height": 1177,
                "thumbnail": "elements/content/thumbs/items-3col-3.jpg"
            },
            {
                "url": "elements/content/tpl/content-4col.html",
                "height": 686,
                "thumbnail": "elements/content/thumbs/content-4col.jpg"
            },
            {
                "url": "elements/content/tpl/content-3col.html",
                "height": 687,
                "thumbnail": "elements/content/thumbs/content-3col.jpg"
            },
            {
                "url": "elements/content/tpl/content-collapse.html",
                "height": 803,
                "thumbnail": "elements/content/thumbs/content-collapse.jpg"
            },
            {
                "url": "elements/content/tpl/content-link-img.html",
                "height": 312,
                "thumbnail": "elements/content/thumbs/content-link-img.jpg"
            },
        ],
        "Diagrams": [
            {
                "url": "elements/diagrams/tpl/diagram-full.html",
                "height": 1216,
                "thumbnail": "elements/diagrams/thumbs/diagram-full.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-full-2.html",
                "height": 1072,
                "thumbnail": "elements/diagrams/thumbs/diagram-full-2.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-half-right.html",
                "height": 850,
                "thumbnail": "elements/diagrams/thumbs/diagram-half-right.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-half-left.html",
                "height": 851,
                "thumbnail": "elements/diagrams/thumbs/diagram-half-left.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-full-3.html",
                "height": 1151,
                "thumbnail": "elements/diagrams/thumbs/diagram-full-3.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-full-4.html",
                "height": 1201,
                "thumbnail": "elements/diagrams/thumbs/diagram-full-4.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-horiz-full.html",
                "height": 1254,
                "thumbnail": "elements/diagrams/thumbs/diagram-horiz-full.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-horiz-full-2.html",
                "height": 1091,
                "thumbnail": "elements/diagrams/thumbs/diagram-horiz-full-2.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-horiz-full-3.html",
                "height": 1304,
                "thumbnail": "elements/diagrams/thumbs/diagram-horiz-full-3.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-horiz-half-right.html",
                "height": 776,
                "thumbnail": "elements/diagrams/thumbs/diagram-horiz-half-right.jpg"
            },
            {
                "url": "elements/diagrams/tpl/diagram-horiz-half-left.html",
                "height": 722,
                "thumbnail": "elements/diagrams/thumbs/diagram-horiz-half-left.jpg"
            }
        ],
        "Download": [
            {
                "url": "elements/download/tpl/download-center-app.html",
                "height": 823,
                "thumbnail": "elements/download/thumbs/download-center-app.jpg"
            },
            {
                "url": "elements/download/tpl/download-center-app-img.html",
                "height": 920,
                "thumbnail": "elements/download/thumbs/download-center-app-img.jpg"
            },
            {
                "url": "elements/download/tpl/download-half.html",
                "height": 744,
                "thumbnail": "elements/download/thumbs/download-half.jpg"
            },
            {
                "url": "elements/download/tpl/download-half-app-img.html",
                "height": 747,
                "thumbnail": "elements/download/thumbs/download-half-app-img.jpg"
            },
            {
                "url": "elements/download/tpl/download-half-2.html",
                "height": 699,
                "thumbnail": "elements/download/thumbs/download-half-2.jpg"
            },
            {
                "url": "elements/download/tpl/download-line.html",
                "height": 384,
                "thumbnail": "elements/download/thumbs/download-line.jpg"
            },
            {
                "url": "elements/download/tpl/download-line-2.html",
                "height": 675,
                "thumbnail": "elements/download/thumbs/download-line-2.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-circle-left.html",
                "height": 456,
                "thumbnail": "elements/download/thumbs/download-marker-circle-left.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-circle-right.html",
                "height": 456,
                "thumbnail": "elements/download/thumbs/download-marker-circle-right.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-arrow-left.html",
                "height": 434,
                "thumbnail": "elements/download/thumbs/download-marker-arrow-left.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-arrow-right.html",
                "height": 434,
                "thumbnail": "elements/download/thumbs/download-marker-arrow-right.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-arrow-down.html",
                "height": 583,
                "thumbnail": "elements/download/thumbs/download-marker-arrow-down.jpg"
            },
            {
                "url": "elements/download/tpl/download-marker-arrow-up.html",
                "height": 614,
                "thumbnail": "elements/download/thumbs/download-marker-arrow-up.jpg"
            },
            {
                "url": "elements/download/tpl/download-center-app-img-2.html",
                "height": 898,
                "thumbnail": "elements/download/thumbs/download-center-app-img-2.jpg"
            }
        ],
        "Blog": [
            {
                "url": "elements/blog/tpl/timeline.html",
                "height": 2975,
                "thumbnail": "elements/blog/thumbs/timeline.jpg"
            },
            {
                "url": "elements/blog/tpl/recent-posts-2col.html",
                "height": 1135,
                "thumbnail": "elements/blog/thumbs/recent-posts-2col.jpg"
            },
            {
                "url": "elements/blog/tpl/recent-posts-3col.html",
                "height": 1105,
                "thumbnail": "elements/blog/thumbs/recent-posts-3col.jpg"
            },
            {
                "url": "elements/blog/tpl/recent-posts-4col.html",
                "height": 783,
                "thumbnail": "elements/blog/thumbs/recent-posts-4col.jpg"
            },
            {
                "url": "elements/blog/tpl/single-post.html",
                "height": 1280,
                "thumbnail": "elements/blog/thumbs/single-post.jpg"
            }
        ],
        "Intro": [
            {
                "url": "elements/intro/tpl/intro-half-left-app.html",
                "height": 900,
                "thumbnail": "elements/intro/thumbs/intro-half-left-app.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left.html",
                "height": 721,
                "thumbnail": "elements/intro/thumbs/intro-half-left.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-center.html",
                "height": 882,
                "thumbnail": "elements/intro/thumbs/intro-center.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-right.html",
                "height": 896,
                "thumbnail": "elements/intro/thumbs/intro-right.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-center-img.html",
                "height": 944,
                "thumbnail": "elements/intro/thumbs/intro-center-img.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-items.html",
                "height": 1129,
                "thumbnail": "elements/intro/thumbs/intro-items.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-left-2.html",
                "height": 810,
                "thumbnail": "elements/intro/thumbs/intro-left-2.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left-2.html",
                "height": 810,
                "thumbnail": "elements/intro/thumbs/intro-half-left-2.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left-3.html",
                "height": 921,
                "thumbnail": "elements/intro/thumbs/intro-half-left-3.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-video.html",
                "height": 867,
                "thumbnail": "elements/intro/thumbs/intro-video.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-line.html",
                "height": 392,
                "thumbnail": "elements/intro/thumbs/intro-line.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-left.html",
                "height": 1011,
                "thumbnail": "elements/intro/thumbs/intro-left.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-right-img.html",
                "height": 1034,
                "thumbnail": "elements/intro/thumbs/intro-right-img.jpg"
            },
        ]
    },
    'HeaderTemplate': {
        "Headers": [
            {
                "url": "elements/headers/tpl/header2.html",
                "height": 498,
                "thumbnail": "elements/headers/thumbs/header2.jpg"
            },
            {
                "url": "elements/headers/tpl/header3.html",
                "height": 959,
                "thumbnail": "elements/headers/thumbs/header3.jpg"
            },
            {
                "url": "elements/headers/tpl/header4.html",
                "height": 660,
                "thumbnail": "elements/headers/thumbs/header4.jpg"
            },
            {
                "url": "elements/headers/tpl/header5.html",
                "height": 694,
                "thumbnail": "elements/headers/thumbs/header5.jpg"
            },
            {
                "url": "elements/headers/tpl/header6.html",
                "height": 491,
                "thumbnail": "elements/headers/thumbs/header6.jpg"
            },
            {
                "url": "elements/headers/tpl/header7.html",
                "height": 715,
                "thumbnail": "elements/headers/thumbs/header7.jpg"
            },
            {
                "url": "elements/headers/tpl/header8.html",
                "height": 633,
                "thumbnail": "elements/headers/thumbs/header8.jpg"
            },
            {
                "url": "elements/headers/tpl/header9.html",
                "height": 633,
                "thumbnail": "elements/headers/thumbs/header9.jpg"
            },
            {
                "url": "elements/headers/tpl/header10.html",
                "height": 567,
                "thumbnail": "elements/headers/thumbs/header10.jpg"
            },
            {
                "url": "elements/headers/tpl/header11.html",
                "height": 708,
                "thumbnail": "elements/headers/thumbs/header11.jpg"
            },
        ],
        "Navigation": [
            {
                "url": "elements/navigation/tpl/nav-full-soc.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-full-soc.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-info.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-info.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-info-2.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-info-2.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-info-soc.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-info-soc.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-share.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-share.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-share-2.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-share-2.jpg"
            },
            {
                "url": "elements/navigation/tpl/nav-soc.html",
                "height": 60,
                "thumbnail": "elements/navigation/thumbs/nav-soc.jpg"
            },
        ],
        "Intro": [
            {
                "url": "elements/intro/tpl/intro-half-left-app.html",
                "height": 900,
                "thumbnail": "elements/intro/thumbs/intro-half-left-app.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left.html",
                "height": 721,
                "thumbnail": "elements/intro/thumbs/intro-half-left.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-center.html",
                "height": 882,
                "thumbnail": "elements/intro/thumbs/intro-center.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-right.html",
                "height": 896,
                "thumbnail": "elements/intro/thumbs/intro-right.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-center-img.html",
                "height": 944,
                "thumbnail": "elements/intro/thumbs/intro-center-img.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-items.html",
                "height": 1129,
                "thumbnail": "elements/intro/thumbs/intro-items.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-left-2.html",
                "height": 810,
                "thumbnail": "elements/intro/thumbs/intro-left-2.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left-2.html",
                "height": 810,
                "thumbnail": "elements/intro/thumbs/intro-half-left-2.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-half-left-3.html",
                "height": 921,
                "thumbnail": "elements/intro/thumbs/intro-half-left-3.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-video.html",
                "height": 867,
                "thumbnail": "elements/intro/thumbs/intro-video.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-line.html",
                "height": 392,
                "thumbnail": "elements/intro/thumbs/intro-line.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-left.html",
                "height": 1011,
                "thumbnail": "elements/intro/thumbs/intro-left.jpg"
            },
            {
                "url": "elements/intro/tpl/intro-right-img.html",
                "height": 1034,
                "thumbnail": "elements/intro/thumbs/intro-right-img.jpg"
            },
        ],
    },
    'FooterTemplate': {
        "Footers": [
            {
                "url": "elements/footers/tpl/footer-2col.html",
                "height": 221,
                "thumbnail": "elements/footers/thumbs/footer-2col.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-2col-dark.html",
                "height": 221,
                "thumbnail": "elements/footers/thumbs/footer-2col-dark.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-2col-share.html",
                "height": 221,
                "thumbnail": "elements/footers/thumbs/footer-2col-share.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-2col-share-2.html",
                "height": 221,
                "thumbnail": "elements/footers/thumbs/footer-2col-share-2.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-center.html",
                "height": 401,
                "thumbnail": "elements/footers/thumbs/footer-center.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-center-soc.html",
                "height": 211,
                "thumbnail": "elements/footers/thumbs/footer-center-soc.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-goto.html",
                "height": 321,
                "thumbnail": "elements/footers/thumbs/footer-goto.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-goto-arrow.html",
                "height": 321,
                "thumbnail": "elements/footers/thumbs/footer-goto-arrow.jpg"
            },
            {
                "url": "elements/footers/tpl/footer-goto-fixed.html",
                "height": 401,
                "thumbnail": "elements/footers/thumbs/footer-goto-fixed.jpg"
            }
        ],
    }
}

ELEMENTS = getattr(settings, 'PAGE_BUILDER_PLUGIN_ELEMENTS', DEFAULT_ELEMENTS)

def get_page_builder_elements_by_model(key):
    """
    RUS: Возвращает элементы page_builder, если у них есть ключ, состоящий из url, высоты блока и папки с изображением.
    """
    return ELEMENTS[key] if key in ELEMENTS else {}
