<?php

if ( ! function_exists( 'stal_child_theme_enqueue_scripts' ) ) {
	/**
	 * Function that enqueue theme's child style
	 */
	function stal_child_theme_enqueue_scripts() {
		$main_style = 'stal-main';
		
		wp_enqueue_style( 'stal-child-style', get_stylesheet_directory_uri() . '/style.css', array( $main_style ) );
	}
	
	add_action( 'wp_enqueue_scripts', 'stal_child_theme_enqueue_scripts' );
}