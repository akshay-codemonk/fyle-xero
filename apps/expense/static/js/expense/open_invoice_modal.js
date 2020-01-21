$(".view-invoice-modal").click(function() {
    $.ajax({
        url: $(this).attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function() {
            $("#invoiceModal").modal("show");
        },
        success: function(data) {
            $("#invoice-id").html(data.invoice_id);
            $("#invoice-date").html(data.date);
            $("#invoice-number").html(data.invoice_number);
            $("#contact-name").html(data.contact_name);
            $("#description").html(data.description);

            $(".invoice-details-table tbody").empty();
            data.line_items.forEach(function(line_item) {
                $(".invoice-details-table tbody").append(
                    `<tr>
                        <td>${line_item.account_code}</td>
                        <td>${line_item.amount}</td>
                        <td>${line_item.description}</td>
                    </tr>`
                );
            });
        }
    })
});