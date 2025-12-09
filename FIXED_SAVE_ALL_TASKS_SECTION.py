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
                                            # If parsing fails, set to 7 days from now
                                            deadline_obj = datetime.now() + timedelta(days=7)
                                    else:
                                        # Default: 7 days from now
                                        deadline_obj = datetime.now() + timedelta(days=7)
                                    
                                    # Save task
                                    task_id = add_task(
                                        meeting_id="AI-Extract",
                                        title=task.get('title', 'Untitled'),
                                        details=task.get('details', ''),
                                        department=task.get('department', 'General'),
                                        assigned_to=task.get('assigned_to', 'Unassigned'),
                                        created_by='AI-Agent',
                                        deadline=deadline_obj,  # ← NOW PASSING datetime OBJECT!
                                        category='Regular'
                                    )
                                    
                                    if task_id:
                                        saved_count += 1
                                    else:
                                        failed_count += 1
                                        
                                except Exception as e:
                                    failed_count += 1
                                    st.error(f"❌ Failed to save '{task.get('title', 'Unknown')}': {e}")
                            
                            # Show results
                            if saved_count > 0:
                                st.success(f"✅ Saved {saved_count}/{len(tasks_list)} tasks!")
                            if failed_count > 0:
                                st.warning(f"⚠️ {failed_count} tasks failed to save")
                            
                            st.cache_data.clear()
                            st.rerun()
