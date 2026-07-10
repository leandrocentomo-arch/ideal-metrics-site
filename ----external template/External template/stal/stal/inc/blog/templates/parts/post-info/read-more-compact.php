<?php if ( ! post_password_required() ) { ?>
	<div class="qodef-e-read-more">
		<?php
		if ( stal_post_has_read_more() ) {
			$button_params = array(
				'link'          => get_permalink() . '#more-' . get_the_ID(),
				'button_layout' => 'filled',
				'size'          => 'small',
				'text'          => esc_html__( 'Continue Reading', 'stal' )
			);
		} else {
			$button_params = array(
				'link'          => get_the_permalink(),
				'button_layout' => 'textual',
				'size'          => 'small',
				'text'          => esc_html__( 'Read More', 'stal' )
			);
		}
		
		stal_render_button_element( $button_params ); ?>
	</div>
<?php } ?>