<div id="qodef-page-comments">
	<?php if ( have_comments() ) {
		$comments_number = get_comments_number();
		?>
		<div id="qodef-page-comments-list" class="qodef-m">
			<h3 class="qodef-m-title"><?php echo sprintf( _n( 'Comments:', 'Comments:', $comments_number, 'stal' ), $comments_number ); ?></h3>
			<ul class="qodef-m-comments">
				<?php wp_list_comments( array_unique( array_merge( array( 'callback' => 'stal_get_comments_list_template' ), apply_filters( 'stal_filter_comments_list_template_callback', array() ) ) ) ); ?>
			</ul>
			
			<?php if ( get_comment_pages_count() > 1 ) { ?>
				<div class="qodef-m-pagination qodef--wp">
					<?php the_comments_pagination( array(
						'prev_text'          => stal_get_icon( 'arrow_carrot-left', 'elegant-icons', esc_html__( '< Prev', 'stal' ) ),
						'next_text'          => stal_get_icon( 'arrow_carrot-right', 'elegant-icons', esc_html__( 'Next >', 'stal' ) ),
						'before_page_number' => '0'
					) ); ?>
				</div>
			<?php } ?>
		</div>
	<?php } ?>
	<?php if ( ! comments_open() && get_comments_number() && post_type_supports( get_post_type(), 'comments' ) ) { ?>
		<p class="qodef-page-comments-not-found"><?php esc_html_e( 'Comments are closed.', 'stal' ); ?></p>
	<?php } ?>
	
	<div id="qodef-page-comments-form">
		<?php

		$qodef_commenter = wp_get_current_commenter();
		$qodef_req       = get_option( 'require_name_email' );
		$qodef_aria_req  = ( $qodef_req ? " aria-required='true'" : '' );
		$qodef_consent   = empty( $qodef_commenter['comment_author_email'] ) ? '' : ' checked="checked"';

		$args = array(
			'title_reply_before' => '<h3 id="reply-title" class="comment-reply-title">',
			'title_reply_after'  => '</h3>',
			'title_reply'        => esc_html__( 'Post a comment', 'stal' ),
			'label_submit'       => esc_html__( 'Send comment', 'stal' ),
			'title_reply_to'     => esc_html__( 'Leave a Reply to %s', 'stal' ),
			'comment_field'      => apply_filters( 'stal__filter_comment_form_textarea_field',
				'<textarea id="comment" placeholder="' . esc_attr__( 'WRITE HERE', 'stal' ) . '" name="comment" cols="45" rows="1" aria-required="true"></textarea>' ),
			'fields'             => apply_filters( 'stal__filter_comment_form_default_fields', array(
				'author'  => '<input id="author" name="author" placeholder="' . esc_attr__( 'YOUR NAME', 'stal' ) . '" type="text" value="' . esc_attr( $qodef_commenter['comment_author'] ) . '" ' . $qodef_aria_req . ' />',
				'email'   => '<input id="email" name="email" placeholder="' . esc_attr__( 'E - MAIL', 'stal' ) . '" type="text" value="' . esc_attr( $qodef_commenter['comment_author_email'] ) . '" ' . $qodef_aria_req . ' />',
				'url'    => '<input id="url" name="url" placeholder="' . esc_attr__( 'WEBSITE', 'stal' ) . '" type="text" value="' . esc_attr( $qodef_commenter['comment_author_url'] ) . '" size="30" maxlength="200" />',
				'cookies' => '<p class="comment-form-cookies-consent"><input id="wp-comment-cookies-consent" name="wp-comment-cookies-consent" type="checkbox" value="yes" ' . $qodef_consent . ' />' .
				             '<label for="wp-comment-cookies-consent">' . esc_html__( 'Save my name, email, and website in this browser for the next time I comment.', 'stal' ) . '</label></p>',
			) ),
		);

		comment_form( apply_filters( 'stal_filter_comment_form_args', $args ) ); ?>
	</div>
</div>