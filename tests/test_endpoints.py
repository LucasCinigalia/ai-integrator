"""Testes para os endpoints da API."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.models.schemas import ItemCreate, ItemUpdate


class TestItemsEndpoints:
    """Testes para os endpoints de items."""

    def test_root_endpoint(self, test_client: TestClient):
        """Testa endpoint raiz."""
        response = test_client.get("/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"

    def test_health_check(self, test_client: TestClient):
        """Testa endpoint de health check."""
        response = test_client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_get_items_success(self, test_client: TestClient):
        """Testa listagem de items com sucesso."""
        response = test_client.get("/items")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        first_item = data[0]
        assert "id" in first_item
        assert "name" in first_item
        assert "created_at" in first_item

    def test_get_item_by_id_success(self, test_client: TestClient):
        """Testa busca de item por ID com sucesso."""
        items_response = test_client.get("/items")
        items = items_response.json()

        if items:
            item_id = items[0]["id"]
            response = test_client.get(f"/items/{item_id}")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["id"] == item_id

    def test_get_item_by_id_not_found(self, test_client: TestClient):
        """Testa busca de item inexistente."""
        response = test_client.get("/items/nonexistent-id")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data

    def test_create_item_success(self, test_client: TestClient):
        """Testa criação de item com sucesso."""
        new_item = {"name": "Novo Item Teste", "description": "Descrição do item de teste"}

        response = test_client.post("/items", json=new_item)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == new_item["name"]
        assert data["description"] == new_item["description"]
        assert "id" in data
        assert "created_at" in data

    def test_create_item_validation_error(self, test_client: TestClient):
        """Testa criação de item com dados inválidos."""
        invalid_item = {"name": "", "description": "Descrição"}

        response = test_client.post("/items", json=invalid_item)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_item_success(self, test_client: TestClient):
        """Testa atualização de item com sucesso."""
        items_response = test_client.get("/items")
        items = items_response.json()

        if items:
            item_id = items[0]["id"]
            update_data = {"name": "Item Atualizado", "description": "Nova descrição"}

            response = test_client.put(f"/items/{item_id}", json=update_data)

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == update_data["name"]
            assert data["description"] == update_data["description"]
            assert data["id"] == item_id

    def test_update_item_partial(self, test_client: TestClient):
        """Testa atualização parcial de item."""
        items_response = test_client.get("/items")
        items = items_response.json()

        if items:
            item_id = items[0]["id"]
            original_name = items[0]["name"]
            update_data = {"description": "Apenas descrição atualizada"}

            response = test_client.put(f"/items/{item_id}", json=update_data)

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["name"] == original_name
            assert data["description"] == update_data["description"]

    def test_update_item_not_found(self, test_client: TestClient):
        """Testa atualização de item inexistente."""
        update_data = {"name": "Item Atualizado"}

        response = test_client.put("/items/nonexistent-id", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data

    def test_delete_item_success(self, test_client: TestClient):
        """Testa remoção de item com sucesso."""
        create_response = test_client.post(
            "/items", json={"name": "Item para deletar", "description": "Teste"}
        )
        created_item = create_response.json()
        item_id = created_item["id"]

        response = test_client.delete(f"/items/{item_id}")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = test_client.get(f"/items/{item_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_item_not_found(self, test_client: TestClient):
        """Testa remoção de item inexistente."""
        response = test_client.delete("/items/nonexistent-id")

        assert response.status_code == status.HTTP_404_NOT_FOUND
