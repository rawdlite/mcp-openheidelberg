import asyncio
import logging
from typing import Optional

import aiohttp
from aiohttp import ClientSession

logger = logging.getLogger("matrix")

class MatrixClient:
    def __init__(self, config: dict):
        self.config = config
        self.session: Optional[ClientSession] = None
        self.access_token = None
        self.user_id = None
        self.homeserver_url = config.get("homeserver_url")
        self.username = config.get("username")
        self.password = config.get("password")

    async def connect(self):
        logger.info("Connecting to Matrix server...")
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Login to Matrix
        login_data = {
            "type": "m.login.password",
            "user": self.username,
            "password": self.password
        }
        
        try:
            async with self.session.post(
                f"{self.homeserver_url}/_matrix/client/v3/login",
                json=login_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.access_token = data.get("access_token")
                    self.user_id = data.get("user_id")
                    logger.info(f"Successfully logged in as {self.user_id}")
                else:
                    logger.error(f"Failed to login: {response.status}")
                    raise Exception(f"Login failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error during login: {e}")
            raise

    async def disconnect(self):
        if self.session:
            await self.session.close()
            self.session = None
        logger.info("Disconnected from Matrix server")

    async def send_message(self, room_id: str, message: str):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "msgtype": "m.text",
            "body": message
        }
        
        try:
            async with self.session.post(
                f"{self.homeserver_url}/_matrix/client/v3/rooms/{room_id}/send/m.room.message",
                headers=headers,
                json=body
            ) as response:
                if response.status == 200:
                    logger.info(f"Message sent to room {room_id}")
                    return await response.json()
                else:
                    logger.error(f"Failed to send message: {response.status}")
                    raise Exception(f"Send failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise

    async def get_room_messages(self, room_id: str, limit: int = 10):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with self.session.get(
                f"{self.homeserver_url}/_matrix/client/v3/rooms/{room_id}/messages?limit={limit}",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get messages: {response.status}")
                    raise Exception(f"Get messages failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error getting messages: {e}")
            raise

    async def join_room(self, room_id: str):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.post(
                f"{self.homeserver_url}/_matrix/client/v3/rooms/{room_id}/join",
                headers=headers
            ) as response:
                if response.status == 200:
                    logger.info(f"Successfully joined room {room_id}")
                    return await response.json()
                else:
                    logger.error(f"Failed to join room: {response.status}")
                    raise Exception(f"Join failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error joining room: {e}")
            raise

    async def leave_room(self, room_id: str):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.post(
                f"{self.homeserver_url}/_matrix/client/v3/rooms/{room_id}/leave",
                headers=headers
            ) as response:
                if response.status == 200:
                    logger.info(f"Successfully left room {room_id}")
                    return await response.json()
                else:
                    logger.error(f"Failed to leave room: {response.status}")
                    raise Exception(f"Leave failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error leaving room: {e}")
            raise

    async def create_room(self, room_name: str, is_private: bool = True):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "room_alias_name": room_name,
            "name": room_name,
            "is_direct": is_private
        }
        
        try:
            async with self.session.post(
                f"{self.homeserver_url}/_matrix/client/v3/createRoom",
                headers=headers,
                json=body
            ) as response:
                if response.status == 200:
                    logger.info(f"Successfully created room {room_name}")
                    return await response.json()
                else:
                    logger.error(f"Failed to create room: {response.status}")
                    raise Exception(f"Create room failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error creating room: {e}")
            raise

    async def get_user_info(self, user_id: str):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with self.session.get(
                f"{self.homeserver_url}/_matrix/client/v3/profile/{user_id}",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get user info: {response.status}")
                    raise Exception(f"Get user info failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            raise

    async def get_rooms(self):
        if not self.access_token:
            raise Exception("Not connected to Matrix server")
            
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with self.session.get(
                f"{self.homeserver_url}/_matrix/client/v3/sync",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to get rooms: {response.status}")
                    raise Exception(f"Get rooms failed with status {response.status}")
        except Exception as e:
            logger.error(f"Error getting rooms: {e}")
            raise

    async def chat_loop(self):
        # Placeholder for chat loop functionality
        pass

    async def cleanup(self):
        await self.disconnect()

async def main():
    # Example usage
    config = {
        "homeserver_url": "https://matrix.org",
        "username": "test_user",
        "password": "test_password"
    }
    
    client = MatrixClient(config)
    try:
        await client.connect()
        print("Matrix client connected successfully")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
