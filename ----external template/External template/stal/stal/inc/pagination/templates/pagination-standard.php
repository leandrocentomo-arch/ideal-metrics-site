<?php if ( isset( $query_result ) && intval( $query_result->max_num_pages ) > 1 ) { ?>
	<div class="qodef-m-pagination qodef--standard">
		<div class="qodef-m-pagination-inner">
			<nav class="qodef-m-pagination-items" role="navigation">
				<div class="qodef-m-pagination-item qodef--prev">
					<a href="#" data-paged="1">
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 35 17" style="enable-background:new 0 0 35 17;" xml:space="preserve"><g><path class="st0" d="M7.1,15.5l-0.8,0.8l-4.6-4.7v-0.8l4.6-4.7l0.8,0.8l-3.6,3.8h29.3V1.2h1v10.4H3.5L7.1,15.5z"/></g></svg>
					</a>
				</div>
				<?php for ( $i = 1; $i <= intval( $query_result->max_num_pages ); $i ++ ) {
					$classes     = $i === 1 ? 'qodef--active' : '';
					$formatted_i = sprintf( "%2d", $i );
					?>
					<div class="qodef-m-pagination-item qodef--number qodef--number-<?php echo esc_attr( $i ); ?> <?php echo esc_attr( $classes ); ?>">
						<a href="#" data-paged="<?php echo esc_attr( $i ); ?>"><?php echo esc_html( $formatted_i ); ?></a>
					</div>
				<?php } ?>
				<div class="qodef-m-pagination-item qodef--next">
					<a href="#" data-paged="2">
                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 35 17" style="enable-background:new 0 0 35 17;" xml:space="preserve"><g><path class="st0" d="M32.1,11.7H1.8V1.2h1v9.4h29.3l-3.6-3.8l0.8-0.8l4.6,4.7v0.8l-4.6,4.7l-0.8-0.8L32.1,11.7z"/></g></svg>
					</a>
				</div>
			</nav>
		</div>
	</div>
<?php } ?>