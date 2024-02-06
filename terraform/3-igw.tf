resource "aws_internet_gateway" "flex_app_igw" {

  vpc_id = aws_vpc.flex_app_vpc.id


  tags = {

    Name = "flex_app_igw"

  }

}