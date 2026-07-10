<?php if ( get_the_posts_pagination() !== '' ): ?>

    <div class="qodef-m-pagination qodef--wp">
		<?php
		// Load posts pagination (in order to override template use navigation_markup_template filter hook)
		the_posts_pagination( array(
			'prev_text'          => '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 35 17" style="enable-background:new 0 0 35 17;" xml:space="preserve"><g><path class="st0" d="M7.1,15.5l-0.8,0.8l-4.6-4.7v-0.8l4.6-4.7l0.8,0.8l-3.6,3.8h29.3V1.2h1v10.4H3.5L7.1,15.5z"/></g></svg>',
			'next_text'          => '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 35 17" style="enable-background:new 0 0 35 17;" xml:space="preserve"><g><path class="st0" d="M32.1,11.7H1.8V1.2h1v9.4h29.3l-3.6-3.8l0.8-0.8l4.6,4.7v0.8l-4.6,4.7l-0.8-0.8L32.1,11.7z"/></g></svg>',
			'before_page_number' => '0'
		) ); ?>
    </div>

<?php endif; ?>