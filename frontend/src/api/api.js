// const BASE_URL = "https://coffehouse-web-production.up.railway.app";
const BASE_URL = "http://localhost:8888"; // Uncomment for local development

export async function fetchMenuItems() {
    try {
        const response = await fetch(`${BASE_URL}/menuitems`);
        if (!response.ok) {
            throw new Error("Failed to fetch menu items");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching menu items:", error);
        return []; // Rethrow the error to be handled by the caller
    }
}

export async function fetchBaristas() {
    try {
        const response = await fetch(`${BASE_URL}/baristas`);
        if (!response.ok) {
            throw new Error("Failed to fetch baristas");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching baristas:", error);
        return []; // Rethrow the error to be handled by the caller
    }
}

export async function fetchManagers() {
    try {
        const response = await fetch(`${BASE_URL}/managers`);
        if (!response.ok) {
            throw new Error("Failed to fetch managers");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching managers:", error);
        return []; // Rethrow the error to be handled by the caller
    }
}

export async function fetchOrders() {
    try {
        const response = await fetch(`${BASE_URL}/orders`);
        if (!response.ok) {
            throw new Error("Failed to fetch orders");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching orders:", error);
        return []; // Rethrow the error to be handled by the caller
    }
}

export async function placeRefillOrder(order) {
    try {
        console.log("Placing refill order:", order); // Debugging line
        const response = await fetch(`${BASE_URL}/refill`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(order),
        });
        if (!response.ok) {
          const errorData = await response.json(); // Try to extract error
          throw new Error(`Failed to place refill order: ${errorData.message || "Unknown error"}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error placing refill order:", error);
        throw error; // Rethrow the error to be handled by the caller
    }
}

export async function addBarista(barista) {
    try {
        console.log("Adding barista:", barista); // Debugging line
        const response = await fetch(`${BASE_URL}/baristas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(barista),
        });
        if (!response.ok) {
            throw new Error("Failed to add barista");
        }
        return await response.json();
    } catch (error) {
        console.error("Error adding barista:", error);
        throw error; // Rethrow the error to be handled by the caller
    }
}

export async function updateBarista(barista) {
    try {
        const response = await fetch(`${BASE_URL}/baristas/${barista.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(barista),
        });
        if (!response.ok) {
            throw new Error("Failed to update barista");
        }
        return await response.json();
    } catch (error) {
        console.error("Error updating barista:", error);
        throw error; // Rethrow the error to be handled by the caller
    }
}

export async function deleteBarista(baristaId) {
    try {
        console.log("Deleting barista with ID:", baristaId); // Debugging line
        const response = await fetch(`${BASE_URL}/baristas/${baristaId}`, {
            method: "DELETE",
        });
        if (!response.ok) {
            throw new Error("Failed to delete barista");
        }
        return await response.json();
    } catch (error) {
        console.error("Error deleting barista:", error);
        throw error; // Rethrow the error to be handled by the caller
    }
}

export async function callOpenAILLM(prompt) {
  try {
    const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4",
        messages: [
          {
            role: "system",
            content:
              "Tell me an interesting fact, how it's made, and the health benefits of the given coffee.",
          },
          { role: "user", content: prompt },
        ],
        max_tokens: 300,
        temperature: 0.7,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch OpenAI response");
    }

    const data = await response.json();
    const content = data.choices[0]?.message?.content || "No response.";
    
    return { text: content };

  } catch (error) {
    console.error("Error calling OpenAI API:", error);
    return { text: "Sorry, couldn't load fact right now." };
  }
}


export async function fetchInventory() {
    try {
        const response = await fetch(`${BASE_URL}/inventory`);
        if (!response.ok) {
            throw new Error("Failed to fetch inventory");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching inventory:", error);
        return []; // Rethrow the error to be handled by the caller
    }
}

export async function placeOrder(order) {
    try {
        console.log("Placing order:", order); // Debugging line
        const response = await fetch(`${BASE_URL}/order`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(order),
        });
        if (!response.ok) {
            const errorData = await response.json(); // Try to extract error
            throw new Error(`Failed to place order: ${errorData.message || "Unknown error"}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error placing order:", error);
        throw error; // Rethrow the error to be handled by the caller
    }
}

