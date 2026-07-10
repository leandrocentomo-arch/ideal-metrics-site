<?php
/**
 * Product quantity inputs
 *
 * This template can be overridden by copying it to yourtheme/woocommerce/global/quantity-input.php.
 *
 * HOWEVER, on occasion WooCommerce will need to update template files and you
 * (the theme developer) will need to copy the new files to your theme to
 * maintain compatibility. We try to do this as little as possible, but it does
 * happen. When this occurs the version of the template file will be bumped and
 * the readme will list any important changes.
 *
 * @see     https://docs.woocommerce.com/document/template-structure/
 * @package WooCommerce/Templates
 * @version 3.6.0
 */

defined( 'ABSPATH' ) || exit;

if ( ! isset ( $input_id ) ) {
	$input_id = uniqid( 'quantity_' );
}

if ( $max_value && $min_value === $max_value ) {
	?>
	<div class="qodef-quantity-buttons quantity hidden">
		<input type="hidden" id="<?php echo esc_attr( $input_id ); ?>" class="qty" name="<?php echo esc_attr( $input_name ); ?>" value="<?php echo esc_attr( $min_value ); ?>" />
	</div>
	<?php
} else {
	/* translators: %s: Quantity. */
	$label = ! empty( $args['product_name'] ) ? sprintf( esc_html__( '%s quantity', 'stal' ), wp_strip_all_tags( $args['product_name'] ) ) : esc_html__( 'Quantity', 'stal' );
	?>
	<div class="qodef-quantity-buttons quantity">
		<?php do_action( 'woocommerce_before_quantity_input_field' ); ?>
		<label class="screen-reader-text" for="<?php echo esc_attr( $input_id ); ?>"><?php echo esc_attr( $label ); ?></label>
		<span class="qodef-quantity-minus">
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 16 13" style="enable-background:new 0 0 16 13;" xml:space="preserve"><g><path class="st0" d="M13.8,2.8l0.7,0.8l-6.2,6.7L2.1,3.6l0.7-0.8l5.5,5.9L13.8,2.8z"/></g></svg>
        </span>
		<input
				type="text"
				id="<?php echo esc_attr( $input_id ); ?>"
				class="<?php echo esc_attr( join( ' ', (array) $classes ) ); ?> qodef-quantity-input"
				data-step="<?php echo esc_attr( $step ); ?>"
				data-min="<?php echo esc_attr( $min_value ); ?>"
				data-max="<?php echo esc_attr( 0 < $max_value ? $max_value : '' ); ?>"
				name="<?php echo esc_attr( $input_name ); ?>"
                value="<?php echo esc_attr( ! empty( $input_value ) ? $input_value : 0 ); ?>"
				title="<?php echo esc_attr_x( 'Qty', 'Product quantity input tooltip', 'stal' ); ?>"
				size="4"
				inputmode="<?php echo esc_attr( $inputmode ); ?>" />
		<span class="qodef-quantity-plus">
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 16 13" style="enable-background:new 0 0 16 13;" xml:space="preserve"><g><path class="st0" d="M13.5,10.3L8,4.4l-5.5,5.9L1.8,9.4L8,2.8l6.3,6.7L13.5,10.3z"/></g></svg>
        </span>
		<?php do_action( 'woocommerce_after_quantity_input_field' ); ?>
	</div>
	<?php
}
