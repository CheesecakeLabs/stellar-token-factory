// Force Origin header to return access-control-allow-origin header
resource "aws_cloudfront_function" "origin-header" {
  count = var.cloudfront_response_header_policy.force_origin_header ? 1 : 0

  name    = "${var.name_prefix}-origin-header"
  runtime = "cloudfront-js-1.0"
  comment = "Force origin request header to return access-control-allow-origin header"
  publish = true
  code    = file("${path.module}/templates/origin-header.js")
}

resource "aws_cloudfront_response_headers_policy" "origin-header" {

  name    = "${replace(var.website_domain_name, ".", "-")}-response-header"
  comment = "Response header policy"

  cors_config {

    access_control_allow_credentials = var.cloudfront_response_header_policy.access_control_allow_credentials

    access_control_allow_headers {
      items = var.cloudfront_response_header_policy.access_control_allow_headers
    }

    access_control_allow_methods {
      items = var.cloudfront_response_header_policy.access_control_allow_methods
    }

    access_control_allow_origins {
      items = local.allowed_origins
    }

    origin_override = var.cloudfront_response_header_policy.origin_override
  }
}