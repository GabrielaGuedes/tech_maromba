import { Button, Modal } from "antd";
import React, { useEffect, useState } from "react";
import { CONSTANTS } from "../utils/constants";
import { getNotifications, userArrived } from "../utils/endpoints";

interface INotificationsModal {
  isOpen: boolean;
  setIsOpen: (value: boolean) => void;
}

const NotificationsModal: React.FC<INotificationsModal> = ({
  isOpen,
  setIsOpen,
}) => {
  const [notifications, setNotifications] = useState<any>([]);

  useEffect(() => {
    getNotifications(CONSTANTS.userId).then((res) => {
      setNotifications(res);
    });

    const updateNotifications = () => {
      getNotifications(CONSTANTS.userId).then((res) => {
        setNotifications(res);
      });
      setTimeout(() => {
        updateNotifications();
      }, 2000);
    };

    updateNotifications();
  }, []);

  const handleOk = () => {
    setIsOpen(false);
  };

  const handleGoTo = (machineId: any, userId: any) => {
    userArrived(machineId, userId).then((res) => {
      if (res.result.includes("Success")) {
        alert("Tudo pronto!");
        setIsOpen(false);
      } else {
        alert("Ops, algo deu errado. Tente novamente.");
      }
    });
  };

  return (
    <Modal
      title="Notificações"
      visible={isOpen}
      onCancel={() => setIsOpen(false)}
      onOk={handleOk}
    >
      {notifications.map((n: any) => (
        <div
          style={{
            border: "2px solid green",
            padding: 4,
            borderRadius: 2,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: 2,
          }}
        >
          <div style={{ color: "gray", fontStyle: "italic", fontSize: "12px" }}>
            {n[3]}
          </div>
          {n[4]}
          <Button
            onClick={() => handleGoTo(n[2], n[1])}
            type="primary"
            style={{ width: "fit-content" }}
          >
            Ir para exercício
          </Button>
        </div>
      ))}
    </Modal>
  );
};

export default NotificationsModal;
