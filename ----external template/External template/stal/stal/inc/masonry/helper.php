<?php

if ( ! function_exists( 'stal_register_masonry_scripts' ) ) {
    /**
     * Function that include modules 3rd party scripts
     */
    function stal_register_masonry_scripts() {
        wp_register_script( 'isotope', STAL_INC_ROOT . '/masonry/assets/js/plugins/isotope.pkgd.min.js', array( 'jquery' ), false, true );
        wp_register_script( 'packery', STAL_INC_ROOT . '/masonry/assets/js/plugins/packery-mode.pkgd.min.js', array( 'jquery' ), false, true );
    }

    add_action( 'stal_action_before_main_js', 'stal_register_masonry_scripts' );
}

if ( ! function_exists( 'stal_include_masonry_scripts' ) ) {
    /**
     * Function that include modules 3rd party scripts
     */
    function stal_include_masonry_scripts() {
        wp_enqueue_script( 'isotope' );
        wp_enqueue_script( 'packery' );
    }
}

if ( ! function_exists( 'stal_enqueue_masonry_scripts_for_templates' ) ) {
	/**
	 * Function that enqueue modules 3rd party scripts for templates
	 */
	function stal_enqueue_masonry_scripts_for_templates() {
		$post_type = apply_filters( 'stal_filter_allowed_post_type_to_enqueue_masonry_scripts', '' );
		
		if ( ! empty( $post_type ) && is_singular( $post_type ) ) {
			stal_include_masonry_scripts();
		}
	}
	
	add_action( 'stal_action_before_main_js', 'stal_enqueue_masonry_scripts_for_templates' );
}

if ( ! function_exists( 'stal_enqueue_masonry_scripts_for_shortcodes' ) ) {
	/**
	 * Function that enqueue modules 3rd party scripts for shortcodes
	 *
	 * @param $atts array
	 */
	function stal_enqueue_masonry_scripts_for_shortcodes( $atts ) {
		
		if ( isset( $atts['behavior'] ) && $atts['behavior'] == 'masonry' ) {
			stal_include_masonry_scripts();
		}
	}
	
	add_action( 'stal_core_action_list_shortcodes_load_assets', 'stal_enqueue_masonry_scripts_for_shortcodes' );
}

if ( ! function_exists( 'stal_register_masonry_scripts_for_list_shortcodes' ) ) {
    /**
     * Function that add masonry scripts to array
     *
     * @param array $scripts
     *
     * @return array
     */
    function stal_register_masonry_scripts_for_list_shortcodes( $scripts ) {

        $scripts['isotope'] = array(
            'registered'	=> true
        );
        $scripts['packery'] = array(
            'registered'	=> true
        );

        return $scripts;
    }

    add_filter( 'stal_core_filter_register_list_shortcode_scripts', 'stal_register_masonry_scripts_for_list_shortcodes' );
}