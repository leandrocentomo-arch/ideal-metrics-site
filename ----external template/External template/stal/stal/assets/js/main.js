(function ($) {
	"use strict";

	window.qodef = {};

	qodef.body = $('body');
	qodef.html = $('html');
	qodef.windowWidth = $(window).width();
	qodef.windowHeight = $(window).height();
	qodef.scroll = 0;

	$(document).ready(function () {
		qodef.scroll = $(window).scrollTop();
		qodefBrowserDetection.init();
		qodefSwiper.init();
		qodefMagnificPopup.init();
		qodefAnchor.init();
	});

	$(window).resize(function () {
		qodef.windowWidth = $(window).width();
		qodef.windowHeight = $(window).height();
	});

	$(window).scroll(function () {
		qodef.scroll = $(window).scrollTop();
	});

	$(document).on('stal_trigger_get_new_posts', function () {
		qodefSwiper.init();
		qodefMagnificPopup.init();
	});

	/*
     * Browser detection functionality
     */
	var qodefBrowserDetection = {
		init: function () {
			qodefBrowserDetection.addBodyClassName();
		},
		isBrowser: function (name) {
			var isBrowser = false;

			switch (name) {
				case 'chrome':
					isBrowser = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
					break;
				case 'safari':
					isBrowser =/Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
					break;
				case 'firefox':
					isBrowser =navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
					break;
				case 'ie':
					isBrowser =window.navigator.userAgent.indexOf("MSIE ") > 0 || !!navigator.userAgent.match(/Trident.*rv\:11\./);
					break;
				case 'edge':
					isBrowser =/Edge\/\d./i.test(navigator.userAgent);
					break;
			}

			return isBrowser;
		},
		addBodyClassName: function () {
			var browsers = [
				'chrome',
				'safari',
				'firefox',
				'ie',
				'edge',
			];

			$.each(browsers, function (key, value) {
				if (qodefBrowserDetection.isBrowser(value) && typeof qodef.body !== 'undefined') {
					if (value === 'ie') {
						value = 'ms-explorer';
					}

					qodef.body.addClass('qodef-browser--' + value);
				}
			});
		}
	};

	/**
	 * Init swiper slider
	 */
	var qodefSwiper = {
		init: function (settings) {
			this.holder = $('.qodef-swiper-container');

			// Allow overriding the default config
			$.extend(this.holder, settings);

			if (this.holder.length) {
				this.holder.each(function () {
					qodefSwiper.createSlider($(this));
				});
			}
		},
		createSlider: function ($holder) {
			var options = qodefSwiper.getOptions($holder),
				breakpoints = qodefSwiper.getOptions($holder, true),
				events  = qodefSwiper.getEvents($holder);

			var $swiper = new Swiper($holder, Object.assign(options, events));

			// Temporary fix for Elementor because they override global window.Swiper object
			if ($('body').hasClass('elementor-page')) {
				$swiper.params.breakpoints = breakpoints;

				var isInViewport = false,
					previousViewportValue = 0;

				$.each(breakpoints, function (key, value) {

					if (parseInt(key, 10) >= qodef.windowWidth && !isInViewport) {
						$swiper.params.slidesPerView = previousViewportValue;

						isInViewport = true;
					}

					previousViewportValue = value.slidesPerView;
				});

				$swiper.update();
			}
		},
		getOptions: function ($holder, returnBreakpoints) {
			var sliderOptions = typeof $holder.data('options') !== 'undefined' ? $holder.data('options') : {},
				spaceBetween = sliderOptions.spaceBetween !== undefined && sliderOptions.spaceBetween !== '' ? sliderOptions.spaceBetween : 0,
				slidesPerView = sliderOptions.slidesPerView !== undefined && sliderOptions.slidesPerView !== '' ? parseInt(sliderOptions.slidesPerView, 10) : 1,
				centeredSlides = sliderOptions.centeredSlides !== undefined && sliderOptions.centeredSlides !== '' ? sliderOptions.centeredSlides : false,
				loop = sliderOptions.loop !== undefined && sliderOptions.loop !== '' ? sliderOptions.loop : true,
				autoplay = sliderOptions.autoplay !== undefined && sliderOptions.autoplay !== '' ? sliderOptions.autoplay : true,
				speed = sliderOptions.speed !== undefined && sliderOptions.speed !== '' ? parseInt(sliderOptions.speed, 10) : 5000,
				speedAnimation = sliderOptions.speedAnimation !== undefined && sliderOptions.speedAnimation !== '' ? parseInt(sliderOptions.speedAnimation, 10) : 800,
				slideAnimation = sliderOptions.slideAnimation !== undefined && sliderOptions.slideAnimation !== '' ? sliderOptions.slideAnimation : '',
				customStages = sliderOptions.customStages !== undefined && sliderOptions.customStages !== '' ? sliderOptions.customStages : false,
				outsideNavigation = sliderOptions.outsideNavigation !== undefined && sliderOptions.outsideNavigation === 'yes',
				nextNavigation = outsideNavigation ? '.swiper-button-next-' + sliderOptions.unique : $holder.find('.swiper-button-next'),
				prevNavigation = outsideNavigation ? '.swiper-button-prev-' + sliderOptions.unique : $holder.find('.swiper-button-prev'),
				pagination = $holder.find('.swiper-pagination');

			if (autoplay !== false && speed !== 5000) {
				autoplay = {
					delay: speed
				};
			}

			var slidesPerView1440 = sliderOptions.slidesPerView1440 !== undefined && sliderOptions.slidesPerView1440 !== '' ? parseInt(sliderOptions.slidesPerView1440, 10) : 5,
				slidesPerView1366 = sliderOptions.slidesPerView1366 !== undefined && sliderOptions.slidesPerView1366 !== '' ? parseInt(sliderOptions.slidesPerView1366, 10) : 4,
				slidesPerView1024 = sliderOptions.slidesPerView1024 !== undefined && sliderOptions.slidesPerView1024 !== '' ? parseInt(sliderOptions.slidesPerView1024, 10) : 3,
				slidesPerView768 = sliderOptions.slidesPerView768 !== undefined && sliderOptions.slidesPerView768 !== '' ? parseInt(sliderOptions.slidesPerView768, 10) : 2,
				slidesPerView680 = sliderOptions.slidesPerView680 !== undefined && sliderOptions.slidesPerView680 !== '' ? parseInt(sliderOptions.slidesPerView680, 10) : 1,
				slidesPerView480 = sliderOptions.slidesPerView480 !== undefined && sliderOptions.slidesPerView480 !== '' ? parseInt(sliderOptions.slidesPerView480, 10) : 1;

			if (!customStages) {
				if (slidesPerView < 2) {
					slidesPerView1440 = slidesPerView;
					slidesPerView1366 = slidesPerView;
					slidesPerView1024 = slidesPerView;
					slidesPerView768 = slidesPerView;
				} else if (slidesPerView < 3) {
					slidesPerView1440 = slidesPerView;
					slidesPerView1366 = slidesPerView;
					slidesPerView1024 = slidesPerView;
				} else if (slidesPerView < 4) {
					slidesPerView1440 = slidesPerView;
					slidesPerView1366 = slidesPerView;
				} else if (slidesPerView < 5) {
					slidesPerView1440 = slidesPerView;
				}
			}

			var breakpoints = {
				// when window width is < 481px
				0: {
					slidesPerView: slidesPerView480
				},
				// when window width is >= 481px
				481: {
					slidesPerView: slidesPerView680
				},
				// when window width is >= 681px
				681: {
					slidesPerView: slidesPerView768
				},
				// when window width is >= 769px
				769: {
					slidesPerView: slidesPerView1024
				},
				// when window width is >= 1025px
				1025: {
					slidesPerView: slidesPerView1366
				},
				// when window width is >= 1367px
				1367: {
					slidesPerView: slidesPerView1440
				},
				// when window width is >= 1441px
				1441: {
					slidesPerView: slidesPerView
				}
			};

			var options = {
				slidesPerView: slidesPerView,
				centeredSlides: centeredSlides,
				spaceBetween: spaceBetween,
				autoplay: autoplay,
				loop: loop,
				speed: speedAnimation,
				navigation: {nextEl: nextNavigation, prevEl: prevNavigation},
				pagination: {el: pagination, type: 'bullets', clickable: true},
				breakpoints: breakpoints
			};
			
			if ( slideAnimation.length ) {
				switch (slideAnimation) {
					case 'fade':
						options.effect     = 'fade';
						options.fadeEffect = {
							crossFade: true
						};
						break;
				}
			}

			if (returnBreakpoints) {
				return breakpoints;
			} else {
				return Object.assign(options, qodefSwiper.getSliderDatas($holder));
			}
		},
		getSliderDatas: function ($holder) {
			var dataList = $holder.data(),
				returnValue = {};

			for (var property in dataList) {
				if (dataList.hasOwnProperty(property)) {
					// It's required to be different from data options because da options are all options from shortcode element
					if (property !== 'options' && typeof dataList[property] !== 'undefined' && dataList[property] !== '') {
						returnValue[property] = dataList[property];
					}
				}
			}

			return returnValue;
		},
		getEvents: function ($holder) {
			return {
				on: {
					init: function () {
						$holder.addClass('qodef-swiper--initialized');
					}
				}
			};
		}
	};

	qodef.qodefSwiper = qodefSwiper;

	/**
	 * Init magnific popup galleries
	 */
	var qodefMagnificPopup = {
		init: function (settings) {
			this.holder = $('.qodef-magnific-popup');

			// Allow overriding the default config
			$.extend(this.holder, settings);

			if (this.holder.length) {
				this.holder.each(function () {
					var $thisPopup = $(this);

					if ($thisPopup.hasClass('qodef-popup-item')) {
						qodefMagnificPopup.initSingleImagePopup($thisPopup);
					} else if ($thisPopup.hasClass('qodef-popup-gallery')) {
						qodefMagnificPopup.initGalleryPopup($thisPopup);
					}
				});
			}
		},
		initSingleImagePopup: function ($popup) {
			var type = $popup.data('type');

			$popup.magnificPopup({
				type: type,
				titleSrc: 'title',
				image: {
					cursor: null
				}
			});
		},
		initGalleryPopup: function ($popup) {
			var $items = $popup.find('.qodef-popup-item'),
				itemsFormatted = qodefMagnificPopup.generateGalleryItems($items);

			$items.each(function (index) {
				var $this = $(this);
				$this.magnificPopup({
					items: itemsFormatted,
					gallery: {
						enabled: true,
					},
					index: index,
					type: 'image',
					image: {
						cursor: null
					}
				});
			});
		},
		generateGalleryItems: function ($items) {
			var itemsFormatted = [];

			if ($items.length) {
				$items.each(function () {
					var $thisItem = $(this);
					var itemFormatted = {
						src: $thisItem.attr('href'),
						title: $thisItem.attr('title'),
						type: $thisItem.data('type')
					};
					itemsFormatted.push(itemFormatted);
				});
			}

			return itemsFormatted;
		}
	};

	qodef.qodefMagnificPopup = qodefMagnificPopup;

	var qodefAnchor = {
		items: '',
		init: function (settings) {
			this.holder = $('.qodef-anchor');

			// Allow overriding the default config
			$.extend(this.holder, settings);

			if (this.holder.length) {
				qodefAnchor.items = this.holder;

				qodefAnchor.clickTrigger();

				$(window).on('load', function () {
					qodefAnchor.checkAnchorOnScroll();
					qodefAnchor.checkAnchorOnLoad();
				});
			}
		},
		clickTrigger: function () {
			qodefAnchor.items.on('click', function (e) {
				var $anchorItem = qodefAnchor.getAnchorItem(this),
					anchorURL = $anchorItem.attr('href'),
					hash = $anchorItem.prop('hash').split('#')[1],
					pageURL = window.location.href,
					pageHash = pageURL.indexOf('#') > -1 ? pageURL.split('#')[1] : 0;

				if (
					anchorURL.indexOf('http') < 0
					|| anchorURL === pageURL
					|| (pageHash !== 0 && anchorURL.substring(0, anchorURL.length - hash.length - 1) === pageURL.substring(0, pageURL.length - pageHash.length - 1))
					|| (pageHash === 0 && anchorURL.substring(0, anchorURL.length - hash.length - 1) === pageURL)
				) {
					e.preventDefault();
				}

				qodefAnchor.animateScroll($anchorItem, hash);
			});
		},
		checkAnchorOnLoad: function () {
			var hash = window.location.hash.split('#')[1];

			if (typeof hash !== 'undefined' && hash !== '' && qodefAnchor.items.length) {
				qodefAnchor.items.each(function () {
					var $anchorItem = qodefAnchor.getAnchorItem(this);

					if ($anchorItem.attr('href').indexOf(hash) > -1) {
						qodefAnchor.animateScroll($anchorItem, hash);
					}
				});
			}
		},
		checkAnchorOnScroll: function () {

			if (qodef.windowWidth > 1024) {
				var $target = $('#qodef-page-inner *[id]');

				if ($target.length) {
					$target.each(function () {
						var $currentTarget = $(this),
							$anchorItem = $('[href*="#' + $currentTarget.attr('id') + '"]');

						if ($anchorItem.length) {
							if (qodefAnchor.isTargetInView($currentTarget)) {
								qodefAnchor.setActiveState($anchorItem);
							}

							$(window).scroll(function () {
								if (qodefAnchor.isTargetInView($currentTarget)) {
									qodefAnchor.setActiveState($anchorItem);
								} else {
									$anchorItem.removeClass(qodefAnchor.getItemClasses($anchorItem));
								}
							});
						}
					});
				}
			}
		},
		isTargetInView: function ($target) {
			var rect = $target[0].getBoundingClientRect(),
				percentVisible = 20,
				windowHeight = (window.innerHeight || document.documentElement.clientHeight);

			return !(
				Math.floor(100 - (((rect.top >= 0 ? 0 : rect.top) / +-(rect.height / 1)) * 100)) < percentVisible ||
				Math.floor(100 - ((rect.bottom - windowHeight) / rect.height) * 100) < percentVisible
			);
		},
		getAnchorItem: function (item) {
			var isItemLink = item.tagName === 'A';

			return isItemLink ? $(item) : $(item).children('a');
		},
		animateScroll: function ($item, hash) {
			var $target = hash !== '' ? $('[id="' + hash + '"]') : '';

			if ($target.length) {
				var targetPosition = $target.offset().top,
					scrollAmount = targetPosition - qodefAnchor.getHeaderHeight() - qodefGlobal.vars.adminBarHeight;

				qodefAnchor.setActiveState($item);

				qodef.html.stop().animate({
					scrollTop: Math.round(scrollAmount)
				}, 1000, function () {
					//change hash tag in url
					if (history.pushState) {
						history.pushState(null, '', '#' + hash);
					}
				});

				return false;
			}
		},
		getHeaderHeight: function () {
			var height = 0;

			if (qodef.windowWidth > 1024 && qodefGlobal.vars.headerHeight !== null && qodefGlobal.vars.headerHeight !== '') {
				height = parseInt(qodefGlobal.vars.headerHeight, 10);
			}

			return height;
		},
		setActiveState: function ($item) {
			var isItemLink = !$item.parent().hasClass('qodef-anchor'),
				classes = qodefAnchor.getItemClasses($item);

			qodefAnchor.items.removeClass(classes);

			if (isItemLink) {
				$item.addClass(classes);
			} else {
				$item.parent().addClass(classes);
			}
		},
		getItemClasses: function ($item) {
			// Main anchor item class plus header item classes if item is inside header
			var activeClass = 'qodef-anchor--active',
				menuItemClasses = $item.parents('#qodef-page-header') ? ' current-menu-item current_page_item' : '';

			return activeClass + menuItemClasses;
		}
	};

	qodef.qodefAnchor = qodefAnchor;

})(jQuery);
(function ($) {
    "use strict";

    $(document).ready(function () {
        qodefResizeIframes.init();
        qodefBlogListHoverAnimation.init();
    });

    $(window).on('resize', function () {
        qodefResizeIframes.init();
    });

    $(document).on('stal_trigger_get_new_posts', function (e, holder) {
        if (holder.hasClass('qodef-blog')) {
            qodefReInitMediaElementPostFormats.init(holder);
            qodefResizeIframes.resize(holder);
            qodefBlogListHoverAnimation.init();
        }
    });

    /**
     * Re init media element post formats (audio, video)
     */
    var qodefReInitMediaElementPostFormats = {
        init: function (holder) {
            var $mediaElement = holder.find('.wp-video-shortcode, .wp-audio-shortcode').not('.mejs-container');

            if ($mediaElement.length) {
                $mediaElement.each(function () {
                    var $thisMediaElement = $(this);

                    if (typeof $thisMediaElement.mediaelementplayer === 'function') {
                        $thisMediaElement.mediaelementplayer();
                    }
                });
            }
        }
    };

    /**
     * Resize oembed iframes
     */
    var qodefResizeIframes = {
        init: function () {
            var $holder = $('.qodef-blog');

            if ($holder.length) {
                qodefResizeIframes.resize($holder);
            }
        },

        resize: function (holder) {
            var $iframe = holder.find('.qodef-e-media iframe');

            if ($iframe.length) {
                $iframe.each(function () {
                    var $thisIframe = $(this),
                        width = $thisIframe.attr('width'),
                        height = $thisIframe.attr('height'),
                        newHeight = $thisIframe.width() / width * height;  // rendered width divided by aspect ratio

                    $thisIframe.css('height', newHeight);
                });
            }
        }
    };

    var qodefBlogListHoverAnimation = {
        init: function() {
            var $holder = $('.qodef-blog');
            var $blogItem = $holder.find('article');

            if ( $blogItem.length ) {
                $blogItem.each( function () {
                    var $thisBlogItem = $(this);
                    var $blogItemTitle = $thisBlogItem.find('.qodef-e-title-link');

                    $blogItemTitle.on('mouseenter', function() {
                        $(this).closest('article').addClass('qodef-active-hover');
                    });

                    $blogItemTitle.on('mouseleave', function() {
                        $(this).closest('article').removeClass('qodef-active-hover');
                    })
                });
            }
        }
    };

})(jQuery);
(function ($) {
	"use strict";
	
	$(document).ready(function () {
		qodefFilter.init();
	});
	
	$(document).on('stal_trigger_get_new_posts', function (e, holder) {
		if (holder.hasClass('qodef-filter--on')) {
			qodefFilter.setVisibility(holder, holder.find('.qodef-m-filter-item.qodef--active'), true);
		}
	});
	
	/*
	 **	Init filter functionality
	 */
	var qodefFilter = {
		init: function (settings) {
			this.holder = $('.qodef-filter--on');
			
			// Allow overriding the default config
			$.extend(this.holder, settings);
			
			if (this.holder.length) {
				this.holder.each(function () {
					var $holder = $(this),
						$filterItems = $holder.find('.qodef-m-filter-item');
					
					qodefFilter.extendListHTML($holder);
					qodefFilter.clickEvent($holder, $filterItems);
				});
			}
		},
		extendListHTML: function (holder) {
			if (!holder.children('.qodef-hidden-filter-items').length && !qodefFilter.isMasonryLayout(holder)) {
				holder.append('<div class="qodef-hidden-filter-items"></div>');
			}
		},
		clickEvent: function (holder, filterItems) {
			filterItems.on('click', function (e) {
				e.preventDefault();
				
				var $thisItem = $(this);
				
				if (!$thisItem.hasClass('qodef--active')) {
					holder.addClass('qodef--filter-loading');
					
					filterItems.removeClass('qodef--active');
					$thisItem.addClass('qodef--active');
					
					qodefFilter.setVisibility(holder, $thisItem);
				}
			});
		},
		setVisibility: function (holder, item, triggerEvent) {
			var $hiddenHolder = holder.children('.qodef-hidden-filter-items'),
				hiddenHolderExist = $hiddenHolder.length,
				$hiddenItems = hiddenHolderExist ? $hiddenHolder.children('.qodef-grid-item') : '',
				$itemsHolder = holder.find('.qodef-grid-inner'),
				$items = $itemsHolder.children('.qodef-grid-item'),
				filterTaxonomy = item.data('taxonomy'),
				filterValue = item.data('filter'),
				isShowAllFilter = filterValue === '*',
				filterClass = isShowAllFilter ? filterValue : filterTaxonomy + '-' + filterValue,
				listHasVisibleItems = $items.hasClass(filterClass);
			
			// Additional conditional for gallery layout to check is items exists inside hidden holder
			if (hiddenHolderExist && !listHasVisibleItems && $hiddenItems.hasClass(filterClass)) {
				listHasVisibleItems = true;
			}
			
			// Prevent filtering when show all is active and load more is trigger
			if (triggerEvent && isShowAllFilter) {
				return;
			}
			
			// If items doesn't exist by default trigger load more to load new page
			if (!isShowAllFilter && !listHasVisibleItems && qodefFilter.hasLoadMore(holder)) {
				qodef.body.trigger('stal_trigger_load_more', [holder]);
			} else {
				if (qodefFilter.isMasonryLayout(holder)) {
					$itemsHolder.isotope({filter: isShowAllFilter ? '' : '.' + filterClass});
				} else {
					if (!isShowAllFilter) {
						$items.each(function () {
							var $listItem = $(this),
								listItemClasses = $listItem.attr('class');
							
							if (listItemClasses.indexOf(filterClass) === -1) {
								$listItem.hide(300, 'linear', function(){
									$listItem.appendTo($hiddenHolder);
								});
							}
						});
					}
					
					if ($hiddenItems.length) {
						$hiddenItems.each(function () {
							var $hiddenListItem = $(this),
								hiddenListItemClasses = $hiddenListItem.attr('class');
							
							if (isShowAllFilter) {
								$hiddenListItem.appendTo($itemsHolder).show(300, 'linear');
							} else if (hiddenListItemClasses.indexOf(filterClass) !== -1) {
								$hiddenListItem.appendTo($itemsHolder).show(300, 'linear');
							}
						});
					}
				}
				
				holder.removeClass('qodef--filter-loading');
			}
		},
		isMasonryLayout: function (holder) {
			return holder.hasClass('qodef-layout--masonry');
		},
		hasLoadMore: function (holder) {
			return holder.hasClass('qodef-pagination-type--load-more');
		}
	};

	qodef.qodefFilter = qodefFilter;
	
})(jQuery);
(function ($) {
	'use strict';
	
	$(document).ready(function () {
		qodefJustifiedGallery.init();
	});
	
	$(document).on('stal_trigger_get_new_posts', function () {
		qodefJustifiedGallery.init();
	});
	
	/**
	 * Init justified gallery functionality
	 */
	var qodefJustifiedGallery = {
		init: function () {
			var $holder = $('.qodef-layout--justified-gallery');
			
			if ($holder.length) {
				$holder.each(function () {
					qodefJustifiedGallery.setJustifyGallery($(this));
				});
			}
		},
		setJustifyGallery: function ($holder) {
			var galleryOptions = $holder.data('options'),
				$galleryInner = $holder.children('.qodef-grid-inner'),
				rowHeight = typeof galleryOptions.justified_gallery_row_height !== 'undefined' && galleryOptions.justified_gallery_row_height !== '' ? galleryOptions.justified_gallery_row_height : 150,
				maxRowHeight = typeof galleryOptions.justified_gallery_row_height_max !== 'undefined' && galleryOptions.justified_gallery_row_height_max !== '' ? galleryOptions.justified_gallery_row_height_max : false,
				margin = galleryOptions.space_value * 2,
				justifyTreshold = typeof galleryOptions.justified_gallery_treshold !== 'undefined' && galleryOptions.justified_gallery_treshold !== '' ? galleryOptions.justified_gallery_treshold : 0.75;
			
			$galleryInner.waitForImages(function () {
				if (typeof $galleryInner.justifiedGallery === 'function') {
					$galleryInner.justifiedGallery({
						captions: false,
						rowHeight: rowHeight,
						maxRowHeight: maxRowHeight,
						margins: margin,
						border: 0,
						lastRow: 'nojustify',
						justifyThreshold: justifyTreshold,
						selector: '.qodef-grid-item'
					}).on('jg.complete jg.rowflush', function () {
						var $gal = $(this),
							deducted = false;
						
						$gal.find('.qodef-grid-item').addClass('show').each(function () {
							var $thisItem = $(this);
							
							$thisItem.height(Math.round($thisItem.height()));
							
							if (!deducted && $thisItem.width() === 0) {
								$gal.height($gal.height() - $thisItem.height() - margin);
								
								deducted = true;
							}
						});
					});
				}
				
				$holder.addClass('qodef--justified-gallery-init');
			});
		}
	};

	qodef.qodefJustifiedGallery = qodefJustifiedGallery;
	
})(jQuery);
(function ($) {
	"use strict";
	
	$(document).ready(function () {
		qodefMasonryLayout.init();
	});
	
	$(document).on('stal_trigger_get_new_posts', function (e, $holder) {
		if ($holder.hasClass('qodef-layout--masonry')) {
			qodefMasonryLayout.init();
		}
	});
	
	/**
	 * Init masonry layout
	 */
	var qodefMasonryLayout = {
		init: function (settings) {
			this.holder = $('.qodef-layout--masonry');
			
			// Allow overriding the default config
			$.extend(this.holder, settings);
			
			if (this.holder.length) {
				this.holder.each(function () {
					qodefMasonryLayout.createMasonry($(this));
				});
			}
		},
		createMasonry: function ($holder) {
			var $masonry = $holder.find('.qodef-grid-inner'),
				$masonryItem = $masonry.find('.qodef-grid-item');
			
			$masonry.waitForImages(function () {
				if (typeof $masonry.isotope === 'function') {
					$masonry.isotope({
						layoutMode: 'packery',
						itemSelector: '.qodef-grid-item',
						percentPosition: true,
						masonry: {
							columnWidth: '.qodef-grid-masonry-sizer',
							gutter: '.qodef-grid-masonry-gutter'
						}
					});
					
					if ($holder.hasClass('qodef-items--fixed')) {
						var size = qodefMasonryLayout.getFixedImageSize($masonry, $masonryItem);

						qodefMasonryLayout.setFixedImageProportionSize($masonry, $masonryItem, size);
					}
					
					$masonry.isotope('layout');
				}
				
				$masonry.addClass('qodef--masonry-init');
			});
		},
		getFixedImageSize: function ($holder, $item) {
			var $squareItem = $holder.find('.qodef-item--square');

			if ($squareItem.length) {
				var $squareItemImage = $squareItem.find('img'),
					squareItemImageWidth = $squareItemImage.width(),
					squareItemImageHeight = $squareItemImage.height();

				if (squareItemImageWidth !== squareItemImageHeight) {
					return squareItemImageHeight;
				} else {
					return squareItemImageWidth;
				}
			} else {
				var size = $holder.find('.qodef-grid-masonry-sizer').width(),
					padding = parseInt($item.css('paddingLeft'), 10);

				return (size - 2 * padding); // remove item side padding to get real item size
			}
		},
		setFixedImageProportionSize: function ($holder, $item, size) {
			var padding = parseInt($item.css('paddingLeft'), 10),
				$squareItem = $holder.find('.qodef-item--square'),
				$landscapeItem = $holder.find('.qodef-item--landscape'),
				$portraitItem = $holder.find('.qodef-item--portrait'),
				$hugeSquareItem = $holder.find('.qodef-item--huge-square'),
				isMobileScreen = qodef.windowWidth <= 680;

			$item.css('height', size);

			if ($landscapeItem.length) {
				$landscapeItem.css('height', Math.round(size / 2));
			}

			if ($portraitItem.length) {
				$portraitItem.css('height', Math.round(2 * (size + padding)));
			}

			if (!isMobileScreen) {

				if ($landscapeItem.length) {
					$landscapeItem.css('height', size);
				}

				if ($hugeSquareItem.length) {
					$hugeSquareItem.css('height', Math.round(2 * (size + padding)));
				}
			}
		}
	};

	qodef.qodefMasonryLayout = qodefMasonryLayout;
	
})(jQuery);
(function ($) {
	"use strict";
	
	$(document).ready(function () {
		qodefMobileHeader.init();
	});
	
	/*
	 **	Init mobile header functionality
	 */
	var qodefMobileHeader = {
		init: function () {
			var $holder = $('#qodef-page-mobile-header');
			
			if ($holder.length) {
				qodefMobileHeader.initMobileHeaderOpener($holder);
				qodefMobileHeader.initDropDownMobileMenu();
			}
		},
		initMobileHeaderOpener: function (holder) {
			var $opener = holder.find('#qodef-mobile-header-opener');
		
			if ($opener.length) {
				var $navigation = holder.find('#qodef-mobile-header-navigation');
			
				$opener.on('tap click', function (e) {
					e.preventDefault();
					
					if ($navigation.is(':visible')) {
						$navigation.slideUp(450);
						$opener.removeClass('qodef--opened');
					} else {
						$navigation.slideDown(450);
						$opener.addClass('qodef--opened');
					}
				});
			}
		},
		initDropDownMobileMenu: function(){
            var $dropdownOpener = $('#qodef-mobile-header-navigation .qodef-menu-arrow, #qodef-mobile-header-navigation .qodef-hide-link > a, body:not([class*="stal-core"]) #qodef-mobile-header-navigation .menu-item-has-children > a');

            if ($dropdownOpener.length) {
                $dropdownOpener.each(function () {
                    var $thisItem = $(this);

                    $thisItem.on('tap click', function (e) {
                    	e.preventDefault();
                    	
                        var $thisItemParent = $thisItem.parent(),
                            $thisItemParentSiblingsWithDrop = $thisItemParent.siblings('.menu-item-has-children');

                        if ($thisItemParent.hasClass('menu-item-has-children')) {
                            var $submenu = $thisItemParent.find('ul.sub-menu').first();

                            if ($submenu.is(':visible')) {
                                $submenu.slideUp(450);
                                $thisItemParent.removeClass('qodef--opened');
                            } else {
                                $thisItemParent.addClass('qodef--opened');

                                if ($thisItemParentSiblingsWithDrop.length === 0) {
                                    $thisItemParent.find('.sub-menu').slideUp(400, function () {
                                        $submenu.slideDown(400);
                                    });
                                } else {
                                    $thisItemParent.siblings().removeClass('qodef--opened').find('.sub-menu').slideUp(400, function () {
                                        $submenu.slideDown(400);
                                    });
                                }
                            }
                        }
                    });
                });
            }
		}
	};
	
})(jQuery);
(function ($) {
	
	$(document).ready(function () {
		qodefDefaultNavMenu.init();
	});
	
	var qodefDefaultNavMenu = {
		init: function () {
			var $menuItems = $('.qodef-header-navigation.qodef-header-navigation-initial > ul > li.qodef-menu-item--narrow.menu-item-has-children');
			
			if ($menuItems.length) {
				$menuItems.each(function (i) {
					var thisItem = $(this),
						menuItemPosition = thisItem.offset().left,
						dropdownMenuItem = thisItem.find(' > ul'),
						dropdownMenuWidth = dropdownMenuItem.outerWidth(),
						menuItemFromLeft = $(window).width() - menuItemPosition;

					var dropDownMenuFromLeft;
					
					if (thisItem.find('li.menu-item-has-children').length > 0) {
						dropDownMenuFromLeft = menuItemFromLeft - dropdownMenuWidth;
					}
					
					dropdownMenuItem.removeClass('qodef-drop-down--right');
					
					if (menuItemFromLeft < dropdownMenuWidth || dropDownMenuFromLeft < dropdownMenuWidth) {
						dropdownMenuItem.addClass('qodef-drop-down--right');
					}
				});
			}
		}
	};
	
})(jQuery);

(function ($) {
	"use strict";
	
	$(document).ready(function () {
		qodefPagination.init();
	});
	
	$(window).scroll(function () {
		qodefPagination.scroll();
	});
	
	$(document).on('stal_trigger_load_more', function (e, $holder, nextPage) {
		qodefPagination.triggerLoadMore($holder, nextPage);
	});
	
	/*
	 **	Init pagination functionality
	 */
	var qodefPagination = {
		init: function (settings) {
			this.holder = $('.qodef-pagination--on');
			
			// Allow overriding the default config
			$.extend(this.holder, settings);
			
			if (this.holder.length) {
				this.holder.each(function () {
					var $holder = $(this);
					
					qodefPagination.initPaginationType($holder);
				});
			}
		},
		scroll: function (settings) {
			this.holder = $('.qodef-pagination--on');
			
			// Allow overriding the default config
			$.extend(this.holder, settings);
			
			if (this.holder.length) {
				this.holder.each(function () {
					var $holder = $(this);
					
					if ($holder.hasClass('qodef-pagination-type--infinite-scroll')) {
						qodefPagination.initInfiniteScroll($holder);
					}
				});
			}
		},
		initPaginationType: function ($holder) {
			if ($holder.hasClass('qodef-pagination-type--standard')) {
				qodefPagination.initStandard($holder);
			} else if ($holder.hasClass('qodef-pagination-type--load-more')) {
				qodefPagination.initLoadMore($holder);
			} else if ($holder.hasClass('qodef-pagination-type--infinite-scroll')) {
				qodefPagination.initInfiniteScroll($holder);
			}
		},
		initStandard: function ($holder) {
			var $paginationItems = $holder.find('.qodef-m-pagination-items');
			
			if ($paginationItems.length) {
				var options = $holder.data('options');
				
				$paginationItems.children().each(function () {
					var $thisItem = $(this),
						$itemLink = $thisItem.children('a');
					
					qodefPagination.changeStandardState($holder, options.max_pages_num, 1);
					
					$itemLink.on('click', function (e) {
						e.preventDefault();
						
						if (!$thisItem.hasClass('qodef--active')) {
							qodefPagination.getNewPosts($holder, $itemLink.data('paged'));
						}
					});
				});
			}
		},
		changeStandardState: function ($holder, max_pages_num, nextPage) {
			if ($holder.hasClass('qodef-pagination-type--standard')) {
				var $paginationNav = $holder.find('.qodef-m-pagination-items'),
					$numericItem = $paginationNav.children('.qodef--number'),
					$prevItem = $paginationNav.children('.qodef--prev'),
					$nextItem = $paginationNav.children('.qodef--next');
				
				$numericItem.removeClass('qodef--active').eq(nextPage - 1).addClass('qodef--active');
				
				$prevItem.children().data('paged', nextPage - 1);
				
				if (nextPage > 1) {
					$prevItem.show();
				} else {
					$prevItem.hide();
				}
				
				$nextItem.children().data('paged', nextPage + 1);
				
				if (nextPage === max_pages_num) {
					$nextItem.hide();
				} else {
					$nextItem.show();
				}
			}
		},
		initLoadMore: function ($holder) {
			var $loadMoreButton = $holder.find('.qodef-load-more-button');
			
			$loadMoreButton.on('click', function (e) {
				e.preventDefault();
				
				qodefPagination.getNewPosts($holder);
			});
		},
		triggerLoadMore: function ($holder, nextPage) {
			qodefPagination.getNewPosts($holder, nextPage);
		},
		hideLoadMoreButton: function ($holder, options) {
			if ($holder.hasClass('qodef-pagination-type--load-more') && options.next_page > options.max_pages_num) {
				$holder.find('.qodef-load-more-button').hide();
			}
		},
		initInfiniteScroll: function ($holder) {
			var holderEndPosition = $holder.outerHeight() + $holder.offset().top,
				scrollPosition = qodef.scroll + qodef.windowHeight;
			
			if (!$holder.hasClass('qodef--loading') && scrollPosition > holderEndPosition) {
				qodefPagination.getNewPosts($holder);
			}
		},
		getNewPosts: function ($holder, nextPage) {
			$holder.addClass('qodef--loading');
			
			var $itemsHolder = $holder.children('.qodef-grid-inner');
			var options = $holder.data('options');
			
			qodefPagination.setNextPageValue(options, nextPage, false);
			
			$.ajax({
				type: "GET",
				url: qodefGlobal.vars.restUrl + qodefGlobal.vars.paginationRestRoute,
				data: {
					options: options
				},
				beforeSend: function( request ) {
					request.setRequestHeader( 'X-WP-Nonce', qodefGlobal.vars.paginationNonce );
				},
				success: function (response) {
					
					if (response.status === 'success') {
						qodefPagination.setNextPageValue(options, nextPage, true);
						qodefPagination.changeStandardState($holder, options.max_pages_num, nextPage);
						
						$itemsHolder.waitForImages(function () {
							qodefPagination.addPosts($itemsHolder, response.data, nextPage);
							qodefPagination.reInitMasonryPosts($holder, $itemsHolder);
							
							qodef.body.trigger('stal_trigger_get_new_posts', [$holder]);
						});
						
						qodefPagination.hideLoadMoreButton($holder, options);
					} else {
						console.log(response.message);
					}
				},
				complete: function () {
					$holder.removeClass('qodef--loading');
				}
			});
		},
		setNextPageValue: function (options, nextPage, ajaxTrigger) {
			if (typeof nextPage !== 'undefined' && nextPage !== '' && !ajaxTrigger) {
				options.next_page = nextPage;
			} else if (ajaxTrigger) {
				options.next_page = parseInt(options.next_page, 10) + 1;
			}
		},
		addPosts: function ($itemsHolder, newItems, nextPage) {
			if (typeof nextPage !== 'undefined' && nextPage !== '') {
				$itemsHolder.html(newItems);
			} else {
				$itemsHolder.append(newItems);
			}
		},
		reInitMasonryPosts: function ($holder, $itemsHolder) {
			if ($holder.hasClass('qodef-layout--masonry')) {
				$itemsHolder.isotope('reloadItems').isotope({sortBy: 'original-order'});
				
				setTimeout(function () {
					$itemsHolder.isotope('layout');
				}, 200);
			}
		}
	};

	qodef.qodefPagination = qodefPagination;
	
})(jQuery);
(function ($) {
	"use strict";
	
	$(document).ready(function () {
		qodefWooSelect2.init();
		qodefWooQuantityButtons.init();
		qodefWooMagnificPopup.init();
	});
	
	var qodefWooSelect2 = {
		init: function (settings) {
			this.holder = [];
			this.holder.push({holder: $('#qodef-woo-page .woocommerce-ordering select'), options: {minimumResultsForSearch: Infinity}});
			this.holder.push({holder: $('#qodef-woo-page .variations select'), options: {}});
			this.holder.push({holder: $('#qodef-woo-page #calc_shipping_country'), options: {}});
			this.holder.push({holder: $('#qodef-woo-page .shipping select#calc_shipping_state'), options: {}});
			this.holder.push({holder: $('.widget.widget_archive select'), options: {}});
			this.holder.push({holder: $('.widget.widget_categories select'), options: {}});
			this.holder.push({holder: $('.widget.widget_text select'), options: {}});
			
			// Allow overriding the default config
			$.extend(this.holder, settings);
			
			if (typeof this.holder === 'object') {
				$.each(this.holder, function (key, value) {
					qodefWooSelect2.createSelect2(value.holder, value.options);
				});
			}
		},
		createSelect2: function ($holder, options) {
			if (typeof $holder.select2 === 'function') {
				$holder.select2(options);
			}
		}
	};
	
	var qodefWooQuantityButtons = {
		init: function() {
			$(document).on('click', '.qodef-quantity-minus, .qodef-quantity-plus', function (e) {
				e.stopPropagation();
				
				var $button = $(this),
					$inputField = $button.siblings('.qodef-quantity-input'),
					step = parseFloat($inputField.data('step')),
					max = parseFloat($inputField.data('max')),
                    min = parseFloat($inputField.data('min')),
					minus = false,
                    inputValue = typeof Number.isNaN === 'function' && Number.isNaN(parseFloat($inputField.val())) ? min : parseFloat($inputField.val()),
					newInputValue;
				
				if ($button.hasClass('qodef-quantity-minus')) {
					minus = true;
				}
				
				if (minus) {
					newInputValue = inputValue - step;
					if (newInputValue >= 1) {
						$inputField.val(newInputValue);
					} else {
						$inputField.val(0);
					}
				} else {
					newInputValue = inputValue + step;
					if (max === undefined) {
						$inputField.val(newInputValue);
					} else {
						if (newInputValue >= max) {
							$inputField.val(max);
						} else {
							$inputField.val(newInputValue);
						}
					}
				}
				
				$inputField.trigger('change');
			});
		}
	};

	var qodefWooMagnificPopup = {
		init: function () {
			if (typeof qodef.qodefMagnificPopup === 'object') {
				var $holder = $('.qodef--single.qodef-magnific-popup.qodef-popup-gallery .woocommerce-product-gallery__image');

				if ($holder.length) {
					$holder.each(function () {
						$(this).children('a').attr('data-type', 'image').addClass('qodef-popup-item');
					});

					qodef.qodefMagnificPopup.init();
				}
			}
		}
	}
	
})(jQuery);
