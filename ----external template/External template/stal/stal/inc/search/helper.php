<?php

if ( ! function_exists( 'stal_get_search_page_excerpt_length' ) ) {
	/**
	 * Function that return number of characters for excerpt on search page
	 *
	 * @return int
	 */
	function stal_get_search_page_excerpt_length() {
		$length = apply_filters( 'stal_filter_search_page_excerpt_length', 250 );
		
		return intval( $length );
	}
}
