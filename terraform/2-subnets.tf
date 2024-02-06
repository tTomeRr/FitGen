resource "aws_subnet" "public_subnets" {

  count = length(var.public_subnet_cidrs)

  vpc_id = aws_vpc.flex_app_vpc.id

  cidr_block = element(var.public_subnet_cidrs, count.index)

  availability_zone = element(var.azs, count.index)



  tags = {

    Name = "Public Subnet ${count.index + 1} ${element(var.azs, count.index)}"

  }

}

resource "aws_subnet" "private_subnets" {

  count = length(var.private_subnet_cidrs)

  vpc_id = aws_vpc.flex_app_vpc.id

  cidr_block = element(var.private_subnet_cidrs, count.index)

  availability_zone = element(var.azs, count.index)



  tags = {

    Name = "Private Subnet ${count.index + 1} ${element(var.azs, count.index)}"

  }

}