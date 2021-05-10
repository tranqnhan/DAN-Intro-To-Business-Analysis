const discountCodeInput = document.getElementById("discount-code");
const script = document.getElementById("get-discount-info");
const infoAlert = document.getElementById("info");
infoAlert.style = "display:none;";

const discountInfo = document.getElementById("discount-info");
discountInfo.style = "display:none;";

const finalPrice = document.getElementById("final-price");
const discountAmt = document.getElementById("discount-amt");

const currentPrice = script.getAttribute("price");

discountCodeInput.addEventListener("blur", () => {
    if (discountCodeInput.value.trim() != "") {
        //Setting initial info alert and button display
        infoAlert.style = "display: block;";
        infoAlert.className = "alert alert-info";
        infoAlert.textContent = "Searching for discount...";
        discountInfo.style = "display:none;";
        buyNowBtn.disabled = true;
        addToCartBtn.disabled = true;

        const discountCode = { item_id: script.getAttribute("item-id"), code: discountCodeInput.value };

        getDiscount(discountCode).then(data => {
            if (data.discount_amt != null) {
                discountInfo.style = "display:block;";
                discountAmt.textContent = `\$${data.discount_amt.toFixed(2)} off per item`;
                finalPrice.textContent = `\$${(Number(currentPrice) - Number(data.discount_amt)).toFixed(2)}`;
                infoAlert.className = "alert alert-success";
                infoAlert.textContent = "Discount found!";
            } else {
                infoAlert.className = "alert alert-warning";
                infoAlert.textContent = "Discount not found!";
            }
            setTimeout(() => { buyNowBtn.disabled = false; addToCartBtn.disabled = false}, 500);
        });
    }
});

async function getDiscount(discountCode) {
    const url = `${window.origin}/order/get-discount`;
    const response = await fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(discountCode),
        cache: "no-cache",
        headers: new Headers({ "content-type": "application/json" })
    })
    return response.json();
}