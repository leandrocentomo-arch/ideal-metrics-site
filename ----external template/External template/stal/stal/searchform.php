<?php
// Unique ID for search form fields
$qodef_unique_id = uniqid( 'qodef-search-form-' );
?>
<form role="search" method="get" class="qodef-search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
	<label for="<?php echo esc_attr( $qodef_unique_id ); ?>" class="screen-reader-text"><?php esc_html_e( 'Search for:', 'stal' ); ?></label>
	<div class="qodef-search-form-inner clear">
		<input type="search" id="<?php echo esc_attr( $qodef_unique_id ); ?>" class="qodef-search-form-field" value="" name="s" placeholder="<?php esc_attr_e( 'Search', 'stal' ); ?>" />
		<button type="submit" class="qodef-search-form-button">
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 19.8 19.7" style="enable-background:new 0 0 19.8 19.7;" xml:space="preserve"><g><path class="st0" d="M14.2,11.9L14,12.3l5.3,5.3l-1.7,1.7l-5.3-5.3L12,14.2c-1.3,0.8-2.7,1.2-4.1,1.2c-2.1,0-3.8-0.7-5.3-2.2 C1.2,11.7,0.5,10,0.5,7.9c0-2.1,0.7-3.8,2.2-5.2c1.4-1.4,3.2-2.2,5.3-2.2s3.8,0.7,5.2,2.2c1.4,1.4,2.2,3.2,2.2,5.2 C15.3,9.4,15,10.7,14.2,11.9z M12.1,3.8c-1.1-1.1-2.5-1.7-4.2-1.7c-1.6,0-3,0.6-4.2,1.7C2.6,4.9,2.1,6.3,2.1,7.9 c0,1.6,0.6,3,1.7,4.1c1.1,1.1,2.5,1.7,4.2,1.7c1.6,0,3-0.6,4.2-1.7c1.2-1.2,1.8-2.6,1.8-4.1C13.8,6.3,13.2,5,12.1,3.8z"/></g></svg>
        </button>
	</div>
</form>