function notify(text, type="is-info") {
    bulmaToast.toast({
        message: text,
        position: "top-center",
        type: type,
        pauseOnHover: true,
        closeOnClick: true
    })
}