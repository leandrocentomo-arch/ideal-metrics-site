<?php

if ( ! function_exists( 'stal_load_page_mobile_header' ) ) {
	/**
	 * Function which loads page template module
	 */
	function stal_load_page_mobile_header() {
		// Include mobile header template
		echo apply_filters( 'stal_filter_mobile_header_template', stal_get_template_part( 'mobile-header', 'templates/mobile-header' ) );
	}
	
	add_action( 'stal_action_page_header_template', 'stal_load_page_mobile_header' );
}

if ( ! function_exists( 'stal_register_mobile_navigation_menus' ) ) {
	/**
	 * Function which registers navigation menus
	 */
	function stal_register_mobile_navigation_menus() {
		$navigation_menus = apply_filters( 'stal_filter_register_mobile_navigation_menus', array( 'mobile-navigation' => esc_html__( 'Mobile Navigation', 'stal' ) ) );
		
		if ( ! empty( $navigation_menus ) ) {
			register_nav_menus( $navigation_menus );
		}
	}
	
	add_action( 'stal_action_after_include_modules', 'stal_register_mobile_navigation_menus' );
}