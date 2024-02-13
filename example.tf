variable "name_length" {
    type = string
    default = "2"
    description = "The number of words to put into the random name"
}

resource "random_pet" "server" {
    length = "${var.name_length}"
}

resource "local_file" "random" {
    content = "${random_pet.server.id}\n"
    filename = "${path.module}/random.txt"
}

output "name" {
    value = "${random_pet.server.id}"
}
