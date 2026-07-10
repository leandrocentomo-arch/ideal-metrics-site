<?php

// Hook to include additional content before 404 page content
do_action( 'stal_action_before_404_page_content' );

// Include module content template
echo apply_filters( 'stal_filter_404_page_content_template', stal_get_template_part( '404', 'templates/404-content', '', stal_get_404_page_parameters() ) );

// Hook to include additional content after 404 page content
do_action( 'stal_action_after_404_page_content' );

