<div class="qodef-e-media">
	<?php switch ( get_post_format() ) {
		case 'gallery':
			stal_template_part( 'blog', 'templates/parts/post-format/gallery' );
			break;
		case 'video':
			stal_template_part( 'blog', 'templates/parts/post-format/video' );
			break;
		case 'audio':
			stal_template_part( 'blog', 'templates/parts/post-format/audio' );
			break;
		default:
			stal_template_part( 'blog', 'templates/parts/post-info/image' );
			break;
	} ?>
</div>