function deleteItem(url, id)
{
    data = "id=" + id;
    $.post(url, data, function(data)
    {
        if(data.result)
        {
            window.location.href = window.location.href
        }
    })
}