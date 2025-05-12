document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const bookId = urlParams.get("book_id");
    const price = parseFloat(urlParams.get("price"));
    const token = localStorage.getItem("token");
  
    if (!bookId || !price || !token) {
      alert("No hay información de compra válida");
      return;
    }
  
    // Cargar proveedores
    try {
      const res = await fetch("http://localhost:8000/delivery/");
      const providers = await res.json();
  
      const select = document.getElementById("proveedorSelect");
      providers.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = p.name;
        select.appendChild(option);
      });
    } catch (err) {
      alert("Error al cargar proveedores");
      return;
    }
  
    // Enviar compra al confirmar
    document.getElementById("checkout-form").addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const quantity = parseInt(document.getElementById("cantidad").value);
      const paymentMethod = document.getElementById("metodoPago").value;
      const providerId = document.getElementById("proveedorSelect").value;
  
      if (!quantity || quantity < 1 || !paymentMethod || !providerId) {
        alert("Todos los campos son obligatorios");
        return;
      }
  
      try {
        // 1. Crear compra
        const purchaseRes = await fetch("http://localhost:8000/purchase", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify({
            book_id: bookId,
            quantity: quantity
          })
        });
  
        if (!purchaseRes.ok) throw new Error("Error al crear compra");
  
        const purchase = await purchaseRes.json();
  
        // 2. Crear pago
        const paymentRes = await fetch("http://localhost:8000/payment/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            purchase_id: purchase.id,
            amount: price * quantity,
            payment_method: paymentMethod
          })
        });
  
        if (!paymentRes.ok) throw new Error("Error al procesar el pago");
  
        // 3. Asignar entrega
        const deliveryRes = await fetch("http://localhost:8000/delivery/assign", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            purchase_id: purchase.id,
            provider_id: providerId
          })
        });
  
        if (!deliveryRes.ok) throw new Error("Error al asignar entrega");
  
        alert("✅ Compra completada con éxito");
        window.location.href = "index.html";
      } catch (error) {
        console.error(error);
        alert("❌ Error durante la compra: " + error.message);
      }
    });
  });
  