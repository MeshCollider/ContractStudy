/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache license, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the license for the specific language governing permissions and
 * limitations under the license.
 */
package org.apache.logging.log4j.core.net.mock;

import java.util.ArrayList;
import java.util.List;

public class MockSyslogServer extends Thread {
    protected List<String> messageList;
    protected int port;
    private int numberOfMessagesToReceive;

    public MockSyslogServer(int numberOfMessagesToReceive, int port) {
        this.numberOfMessagesToReceive = numberOfMessagesToReceive;
        this.messageList = new ArrayList<String>();
        this.port = port;
    }

    @Override
    public void run() {

    }

    public void shutdown() {

    }

    public int getNumberOfReceivedMessages() {
        return messageList.size();
    }

    public List<String> getMessageList() {
        return messageList;
    }
}
