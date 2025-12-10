                    try:
                        # ROBUST JSON CLEANING - handles all markdown fence variations
                        import re
                        
                        clean_json = extracted.strip()
                        
                        # Remove ```json ... ``` fence
                        if clean_json.startswith('```json'):
                            clean_json = clean_json[7:]
                            if clean_json.endswith('```'):
                                clean_json = clean_json[:-3]
                        
                        # Remove ``` ... ``` fence (no language)
                        elif clean_json.startswith('```'):
                            clean_json = clean_json[3:]
                            if clean_json.endswith('```'):
                                clean_json = clean_json[:-3]
                        
                        # Strip again
                        clean_json = clean_json.strip()
                        
                        # Find JSON array/object if there's extra text
                        json_match = re.search(r'(\[.*\]|\{.*\})', clean_json, re.DOTALL)
                        if json_match:
                            clean_json = json_match.group(1)
                        
                        # Parse JSON
                        tasks_list = json.loads(clean_json)
                        
                        # Display extracted tasks
                        st.success(f"✅ Extracted {len(tasks_list)} tasks")
                        st.dataframe(pd.DataFrame(tasks_list), use_container_width=True)
                        
                        if st.button("💾 Save All Tasks"):
                            saved_count = 0
                            failed_count = 0
                            
                            for task in tasks_list:
                                try:
                                    # Convert deadline string to datetime
                                    deadline_str = task.get('deadline', 'TBD')
                                    
                                    if deadline_str and deadline_str != 'TBD':
                                        try:
                                            deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%d')
                                        except:
                                            deadline_obj = datetime.now() + timedelta(days=7)
                                    else:
                                        deadline_obj = datetime.now() + timedelta(days=7)
                                    
                                    # Save task
                                    task_id = add_task(
                                        meeting_id="AI-Extract",
                                        title=task.get('title', 'Untitled'),
                                        details=task.get('details', ''),
                                        department=task.get('department', 'General'),
                                        assigned_to=task.get('assigned_to', 'Unassigned'),
                                        created_by='AI-Agent',
                                        deadline=deadline_obj,
                                        category='Regular'
                                    )
                                    
                                    if task_id:
                                        saved_count += 1
                                    else:
                                        failed_count += 1
                                        
                                except Exception as e:
                                    failed_count += 1
                                    st.error(f"❌ Failed to save '{task.get('title', 'Unknown')}': {e}")
                            
                            if saved_count > 0:
                                st.success(f"✅ Saved {saved_count}/{len(tasks_list)} tasks!")
                            if failed_count > 0:
                                st.warning(f"⚠️ {failed_count} tasks failed to save")
                            
                            st.cache_data.clear()
                            st.rerun()
                            
                    except json.JSONDecodeError as e:
                        st.error(f"❌ Failed to parse JSON: {e}")
                        st.code(extracted, language='text')
                        st.info("💡 The AI response contains invalid JSON. Try again or check the raw output above.")
                    except Exception as e:
                        st.error(f"❌ Error processing tasks: {e}")
