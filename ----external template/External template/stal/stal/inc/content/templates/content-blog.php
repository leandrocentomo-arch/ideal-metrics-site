<?php
// Hook to include additional content before page content holder
do_action( 'stal_action_before_page_content_holder' );
?>
<main id="qodef-page-content" class="qodef-grid qodef-layout--template <?php echo esc_attr( stal_get_grid_gutter_classes() ); ?>">
	<div class="qodef-grid-inner clear">
		<?php
		// Include blog template
		echo apply_filters( 'stal_filter_blog_template' , stal_get_template_part( 'blog', 'templates/blog' ) );
		
		// Include page content sidebar
		stal_template_part( 'sidebar', 'templates/sidebar' );
		?>
	</div>
</main>
<?php
// Hook to include additional content after main page content holder
do_action( 'stal_action_after_page_content_holder' );
?>