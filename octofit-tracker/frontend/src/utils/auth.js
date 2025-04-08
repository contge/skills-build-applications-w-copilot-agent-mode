// Utility function to retrieve the token
export function getToken() {
  // Retrieve the token from localStorage
  const token = localStorage.getItem('authToken');
  return token ? `Bearer ${token}` : ''; // Return the token in the required format or an empty string if not found
}
