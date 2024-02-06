data "aws_route53_zone" "primary" {
  name = "tomer-cohen.com"
  private_zone = false
}

resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "tomer-cohen.com"
  type    = "A"

  alias {
    name                   = aws_lb.flex_app_alb.dns_name
    zone_id                = aws_lb.flex_app_alb.zone_id
    evaluate_target_health = true
  }
}