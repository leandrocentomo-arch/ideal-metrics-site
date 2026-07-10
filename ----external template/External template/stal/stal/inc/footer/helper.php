<?php

if ( ! function_exists( 'stal_is_page_footer_enabled' ) ) {
	/**
	 * Function that check is module enabled
	 *
	 * @return bool
	 */
	function stal_is_page_footer_enabled() {
		$is_enabled = stal_is_footer_top_area_enabled() || stal_is_footer_bottom_area_enabled();
		
		return apply_filters( 'stal_filter_enable_page_footer', $is_enabled );
	}
}

if ( ! function_exists( 'stal_load_page_footer' ) ) {
	/**
	 * Function which loads page template module
	 */
	function stal_load_page_footer() {
		
		if ( stal_is_page_footer_enabled() ) {
			// Include footer template
			echo apply_filters( 'stal_filter_footer_template', stal_get_template_part( 'footer', 'templates/footer' ) );
		}
	}
	
	add_action( 'stal_action_page_footer_template', 'stal_load_page_footer' );
}

if ( ! function_exists( 'stal_get_page_footer_sidebars_config' ) ) {
	/**
	 * Function that return config variables for page footer
	 *
	 * @return array
	 */
	function stal_get_page_footer_sidebars_config() {
		
		// Config variables
		$config = apply_filters( 'stal_filter_page_footer_sidebars_config', array(
			'title_class'                   => 'qodef-widget-title',
			'footer_top_sidebars_number'    => 4,
			'footer_top_title_tag'          => 'h5',
			'footer_bottom_sidebars_number' => 2,
			'footer_bottom_title_tag'       => 'h5'
		) );
		
		return $config;
	}
}

if ( ! function_exists( 'stal_get_page_footer_sidebars_config_by_key' ) ) {
	/**
	 * Function that return page footer config variable value by key
	 *
	 * @param $key string - key of config variables array value
	 *
	 * @return string | mixed
	 */
	function stal_get_page_footer_sidebars_config_by_key( $key ) {
		$config = stal_get_page_footer_sidebars_config();
		$value  = '';
		
		if ( ! empty( $key ) && isset( $config[ $key ] ) ) {
			$value = $config[ $key ];
		}
		
		return $value;
	}
}

if ( ! function_exists( 'stal_register_footer_sidebars' ) ) {
	/**
	 * Function that registers theme's footer sidebars area
	 */
	function stal_register_footer_sidebars() {
		
		// Config variables
		$config                 = stal_get_page_footer_sidebars_config();
		$footer_top_sidebars    = array();
		$footer_bottom_sidebars = array();
		
		if ( ! empty( $config ) ) {
			for ( $i = 1; $i <= intval( $config['footer_top_sidebars_number'] ); $i ++ ) {
				$footer_top_sidebars[ 'column_' . $i ] = array(
					'name'        => sprintf( esc_html__( 'Footer Top Area - Column %s', 'stal' ), $i ),
					'description' => sprintf( esc_html__( 'Widgets added here will appear in the %s column of top footer area', 'stal' ), $i ),
					'title_tag'   => $config['footer_top_title_tag']
				);
			}
			
			for ( $i = 1; $i <= intval( $config['footer_bottom_sidebars_number'] ); $i ++ ) {
				$footer_bottom_sidebars[ 'column_' . $i ] = array(
					'name'        => sprintf( esc_html__( 'Footer Bottom Area - Column %s', 'stal' ), $i ),
					'description' => sprintf( esc_html__( 'Widgets added here will appear in the %s column of bottom footer area', 'stal' ), $i ),
					'title_tag'   => $config['footer_bottom_title_tag']
				);
			}
		}
		
		$sidebars = array(
			'footer_top_area'    => $footer_top_sidebars,
			'footer_bottom_area' => $footer_bottom_sidebars
		);
		
		if ( ! empty( $sidebars ) ) {
			foreach ( $sidebars as $sidebar_area => $sidebar_area_value ) {
				foreach ( $sidebar_area_value as $key => $value ) {
					$sidebar_id    = $sidebar_area . '_' . $key;
					
					register_sidebar(
						array(
							'id'            => $sidebar_id,
							'name'          => $value['name'],
							'description'   => $value['description'],
							'before_widget' => '<div id="%1$s" class="widget %2$s" data-area="' . esc_attr( $sidebar_id ) . '">',
							'after_widget'  => '</div>',
							'before_title'  => '<'. esc_attr( $value['title_tag'] ) .' class="'. esc_attr( $config['title_class'] ) .'">',
							'after_title'   => '</'. esc_attr( $value['title_tag'] ) .'>'
						)
					);
				}
			}
		}
	}
	
	add_action( 'widgets_init', 'stal_register_footer_sidebars' );
}

if ( ! function_exists( 'stal_is_footer_top_area_enabled' ) ) {
	/**
	 * Function that check if page footer top area widgets are empty
	 *
	 * @return bool
	 */
	function stal_is_footer_top_area_enabled() {
		$flag = false;
		
		for ( $i = 1; $i <= intval( stal_get_page_footer_sidebars_config_by_key( 'footer_top_sidebars_number' ) ); $i ++ ) {
			$sidebar_id = 'footer_top_area_column_' . $i;
			
			if ( is_active_sidebar( $sidebar_id ) ) {
				$flag = true;
				break;
			}
		}
		
		return apply_filters( 'stal_filter_enable_footer_top_area', $flag );
	}
}

if ( ! function_exists( 'stal_is_footer_bottom_area_enabled' ) ) {
	/**
	 * Function that check if page footer bottom area widgets are empty
	 *
	 * @return bool
	 */
	function stal_is_footer_bottom_area_enabled() {
		$flag = false;
		
		for ( $i = 1; $i <= intval( stal_get_page_footer_sidebars_config_by_key( 'footer_bottom_sidebars_number' ) ); $i ++ ) {
			$sidebar_id = 'footer_bottom_area_column_' . $i;
			
			if ( is_active_sidebar( $sidebar_id ) ) {
				$flag = true;
				break;
			}
		}
		
		return apply_filters( 'stal_filter_enable_footer_bottom_area', $flag );
	}
}

if ( ! function_exists( 'stal_get_footer_top_area_classes' ) ) {
	/**
	 * Function that return classes for page footer top area
	 *
	 * @return string
	 */
	function stal_get_footer_top_area_classes() {
		$classes = apply_filters( 'stal_filter_footer_top_area_classes', 'qodef-content-grid' );
		
		return $classes;
	}
}

if ( ! function_exists( 'stal_get_footer_top_area_columns_classes' ) ) {
	/**
	 * Function that return columns classes for page footer top area
	 *
	 * @return string
	 */
	function stal_get_footer_top_area_columns_classes() {
		$columns_number = stal_get_page_footer_sidebars_config_by_key( 'footer_top_sidebars_number' );
		
		switch ( $columns_number ) {
			case '4':
				$responsive_columns_number = array(
					'qodef-col-num--1024--2',
					'qodef-col-num--768--2',
					'qodef-col-num--680--1',
					'qodef-col-num--480--1'
				);
				break;
			case '3':
				$responsive_columns_number = array(
					'qodef-col-num--768--1',
					'qodef-col-num--680--1',
					'qodef-col-num--480--1'
				);
				break;
			case '2':
				$responsive_columns_number = array(
					'qodef-col-num--680--1',
					'qodef-col-num--480--1'
				);
				break;
			default:
				$responsive_columns_number = array();
				break;
		}
		
		$classes = apply_filters( 'stal_filter_footer_top_area_columns_classes', array_merge( array(
			'qodef-grid',
			'qodef-layout--columns',
			'qodef-responsive--custom',
			'qodef-col-num--' . intval( $columns_number )
		), $responsive_columns_number ) );
		
		return implode( ' ', $classes );
	}
}

if ( ! function_exists( 'stal_get_footer_bottom_area_classes' ) ) {
	/**
	 * Function that return classes for page footer bottom area
	 *
	 * @return string
	 */
	function stal_get_footer_bottom_area_classes() {
		$classes = apply_filters( 'stal_filter_footer_bottom_area_classes', 'qodef-content-grid' );
		
		return $classes;
	}
}

if ( ! function_exists( 'stal_get_footer_bottom_area_columns_classes' ) ) {
	/**
	 * Function that return columns classes for page footer bottom area
	 *
	 * @return string
	 */
	function stal_get_footer_bottom_area_columns_classes() {
		$columns_number = stal_get_page_footer_sidebars_config_by_key( 'footer_bottom_sidebars_number' );
		
		switch ( $columns_number ) {
			case '3':
				$responsive_columns_number = array(
					'qodef-col-num--768--1',
					'qodef-col-num--680--1',
					'qodef-col-num--480--1'
				);
				break;
			case '2':
				$responsive_columns_number = array(
					'qodef-col-num--768--1',
					'qodef-col-num--680--1',
					'qodef-col-num--480--1'
				);
				break;
			default:
				$responsive_columns_number = array();
				break;
		}
		
		$classes = apply_filters( 'stal_filter_footer_bottom_area_columns_classes', array_merge( array(
			'qodef-grid',
			'qodef-layout--columns',
			'qodef-responsive--custom',
			'qodef-col-num--' . intval( $columns_number )
		), $responsive_columns_number ) );
		
		return implode( ' ', $classes );
	}
}