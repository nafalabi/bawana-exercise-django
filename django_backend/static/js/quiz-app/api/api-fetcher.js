import axios from 'axios';
import Cookies from 'js-cookie'; // Library to manage cookies

class ApiFetcher {
  constructor(baseURL) {
    this.api = axios.create({
      baseURL: baseURL,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', // Required for Django session auth
      },
      withCredentials: true, // Allows cookies to be sent with requests
    });
  }

  getCsrfToken() {
    return Cookies.get('csrftoken'); // Fetch CSRF token from cookies
  }

  async get(endpoint, params = {}) {
    try {
      const response = await this.api.get(endpoint, { params });
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }

  async post(endpoint, data) {
    try {
      const response = await this.api.post(endpoint, data, {
        headers: {
          'X-CSRFToken': this.getCsrfToken(), // Include CSRF token in header
        },
      });
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }

  async put(endpoint, data) {
    try {
      const response = await this.api.put(endpoint, data, {
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      });
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }

  async patch(endpoint, data) {
    try {
      const response = await this.api.patch(endpoint, data, {
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      });
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }

  async delete(endpoint) {
    try {
      const response = await this.api.delete(endpoint, {
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
        },
      });
      return response.data;
    } catch (error) {
      return this.handleError(error);
    }
  }

  handleError(error) {
    if (error.response) {
      console.error('API error:', error.response.data);
      return error.response.data;
    } else if (error.request) {
      console.error('No response received:', error.request);
      return { error: 'No response received from the server.' };
    } else {
      console.error('Error setting up request:', error.message);
      return { error: 'Error setting up request.' };
    }
  }
}

export default ApiFetcher;
