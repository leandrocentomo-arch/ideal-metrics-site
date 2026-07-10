<article <?php post_class( 'qodef-search-item qodef-e' ); ?>>
	<div class="qodef-e-inner">
		<?php
		// Include post title
		stal_template_part( 'search', 'templates/parts/post-info/image' ); ?>
		<div class="qodef-e-content">
            <div class="qodef-e-info qodef-info--top">
                <?php
                // Include post date info
                stal_template_part( 'blog', 'templates/parts/post-info/date' );

                // Include post category info
                stal_template_part( 'blog', 'templates/parts/post-info/author' );
                ?>
            </div>
			<?php
			// Include post title
			stal_template_part( 'search', 'templates/parts/post-info/title' );
			
			// Include post excerpt
			stal_template_part( 'search', 'templates/parts/post-info/excerpt' );
			?>
		</div>
	</div>
</article>